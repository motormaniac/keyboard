use rand;
use crate::fileio::AllData;

#[derive(Debug)]
pub struct Individual {
    pub layout:Vec<&'static str>,
    pub fitness:f64,
}

impl Clone for Individual {
    fn clone(&self) -> Self {
        Individual {
            layout: self.layout.clone(),
            fitness: self.fitness.clone(),
        }
    }
}

impl Individual {
    pub fn random(all_data:&AllData) -> Self {
        //List of strings where the index represents a keyboard location
        //Corresponds with the indexes of this list:
        //["000", "010", "020", "030", "040",
        // "100", "110", "120", "130", "140",
        // "200", "210", "220", "230", "240",
        // "001", "011", "021", "031", "041",
        // "101", "111", "121", "131", "141",
        // "201", "211", "221", "231", "241",]
        let mut new_individual = Individual {
            layout: vec![
                "SPACE","A","B","C","D",
                "E","F","G","H","I",
                "J","K","L","M","N",
                "SPACE","O","P","Q","R",
                "S","T","U","V","W",
                "X","Y","Z","_","_"],
            fitness: 0f64,
        };
        for _ in 0..15 {
            new_individual.switch();
        };
        new_individual.calc_fitness(all_data);
        new_individual
    }
    pub fn from_layout(layout:Vec<&'static str>, all_data:&AllData) -> Self {
        let mut new_individual = Individual{layout,fitness:0f64};
        new_individual.calc_fitness(all_data);
        new_individual
    }
    pub fn switch(&mut self) {
        let layout = &mut self.layout;
        let a = rand::random_range(0..30);
        let b = rand::random_range(0..30);
        if layout[a] == "SPACE" || layout[b] == "SPACE" {
            layout.swap(a%15, b%15);
            layout.swap((a%15)+15, (b%15)+15);
        } else {
            layout.swap(a, b);
        }
    }
    pub fn calc_fitness(&mut self, all_data:&AllData) -> f64 {
        let mut fitness:f64 = 0f64;
        for (index, letter) in self.layout.iter().enumerate() {
            //calculate single
            if *letter == "_" {  //blank letters contribute nothing to fitness
                continue;
            }
            let single_key = all_data.single_key_data[index];
            let single_letter = all_data.single_letter_data[*letter];
            fitness += single_key * single_letter;

            for (index2, letter2) in self.layout.iter().enumerate().skip(index+1) {
                if *letter2 == "_" {
                    continue;
                }
                if *letter == "SPACE" && *letter2 == "SPACE" {
                    continue;
                }
                //There should never be the same character twice in a row
                let combo_key = all_data.combination_key_data
                    [all_data.single_key_names[index]][all_data.single_key_names[index2]].unwrap();
                //there should never be the same key twice in a row
                let combo_letter = all_data.combination_letter_data
                    [*letter][*letter2].expect(&format!("letter1:{:?}, letter2:{:?}",letter, letter2));
                fitness += combo_key * combo_letter;
            }
        }
        self.fitness = fitness;
        fitness
    }

    // Uses the PMX crossover algorithm
    pub fn crossover(indiv1:&Individual, indiv2:&Individual, all_data:&AllData) -> (Individual, Individual) {
        //Returns: (Cleaned vector, old space index, old empty index1, old empty index2)
        fn clean_layout<'a>(layout:&Vec<&'a str>) -> Vec<&'a str> {
            let mut clean_layout:Vec<&str> = Vec::new();

            for key in layout {
                if *key == "SPACE" || *key == "_" {
                    continue;
                }
                clean_layout.push(*key);
            };
            clean_layout
        }

        let clean_layout1 = clean_layout(&indiv1.layout);
        let clean_layout2 = clean_layout(&indiv2.layout);

        assert_eq!(clean_layout1.len(), clean_layout2.len());
        
        // assume both layouts are the same length
        let mut left = rand::random_range(0..clean_layout1.len());
        let mut right = rand::random_range(0..clean_layout1.len());
        if left > right { //ensure left < right
            (left, right) = (right, left);
        }
        
        let slice1 = &clean_layout1[left..=right];
        let slice2 = &clean_layout2[left..=right];
        let mut new_layout1:Vec<&str> = Vec::new();
        let mut new_layout2:Vec<&str> = Vec::new();

        //recursive function that performs the mapping part of PMX
        //Checks if the character exists in start_slice. If so, use the character in end_slice.
        fn generate_unique_char<'a>(test_char:&'a str, start_slice: &[&str], end_slice: &[&'a str]) -> &'a str{
            // Find which index in the slice contains 
            let search_index= start_slice.iter().position(|x| x == &test_char);
                match search_index {
                    None => {
                        // this character does not exist in slice2, which means there are no duplicates.
                        //It is safe to use this character.
                        test_char
                    },
                    Some(index) => {
                        // There is a duplicate! Get the corresponding index in end_slice, then check it.
                        generate_unique_char(end_slice[index], start_slice, end_slice)
                    }
                }
        }

        //filling new_layout1
        for i in 0..clean_layout1.len() {
            if i < left || right < i{
                // Remember that you switch slices 1 and 2. 
                let new_char = generate_unique_char(clean_layout1[i], slice2, slice1);
                new_layout1.push(new_char);
            } else if left <= i && i <= right {
                new_layout1.push(slice2[i-left]);
            } else {
                unreachable!()
            }
        }

        //filling new_layout2
        for i in 0..clean_layout2.len() {
            if i < left || right < i{
                // Remember that you switch slices 1 and 2. 
                let new_char = generate_unique_char(clean_layout2[i], slice1, slice2);
                new_layout2.push(new_char);
            } else if left <= i && i <= right {
                new_layout2.push(slice1[i-left]);
            } else {
                unreachable!()
            }
        }

        //put removed indexes back in
        for (index, key) in indiv1.layout.iter().enumerate() {
            if *key == "SPACE" || *key == "_" {
                if index == new_layout1.len() {
                    new_layout1.push(*key);
                    continue;
                }
                new_layout1.insert(index, *key);
            }
        }

        //put removed indexes back in
        for (index, key) in indiv2.layout.iter().enumerate() {
            if *key == "SPACE" || *key == "_" {
                if index == new_layout2.len() {
                    new_layout2.push(*key);
                    continue;
                }
                new_layout2.insert(index, *key);
            }
        }

        (Individual::from_layout(new_layout1, all_data), Individual::from_layout(new_layout2, all_data))
    }
}

