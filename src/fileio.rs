use std::fs::read_to_string;
use std::collections::HashMap;

pub struct AllData {
    pub single_key_names:Vec<&'static str>,
    pub single_key_data:Vec<f64>,
    pub combination_key_data:HashMap<String, HashMap<String, Option<f64>>>,
    pub single_letter_data:HashMap<String, f64>,
    pub combination_letter_data:HashMap<String, HashMap<String, Option<f64>>>,
}

pub fn read_combination_data(filepath:& str) -> HashMap<String, HashMap<String, Option<f64>>> {
    let contents:&str = &read_to_string(filepath)
        .expect("Invalid filepath");

    let mut output:HashMap<String, HashMap<String, Option<f64>>> = HashMap::new();

    //windows uses \r\n to go to the next line
    let lines:Vec<&str> = contents.split("\r\n").collect();
    let mut headers:Vec<&str> = lines[0].split("\t").collect();
    headers.remove(0); //remove the _ in the beginning
    for line in &lines[1..] {
        let words:Vec<&str> = line.split("\t").collect();
        for (i, word) in words[1..].iter().enumerate() {
            let key1:&str = headers[i];
            let key2:&str = words[0];

            let value:Option<f64> = if word == &"NA" {
                None
            } else {
                match word.parse() {
                    Ok(x) => Some(x),
                    Err(_) => {
                        panic!("{word}");
                    }
                }
            };

            if output.get(key1) == None {
                output.insert(String::from(key1), HashMap::new());
            }
            let submap = output.get_mut(key1).unwrap();
            submap.insert(String::from(key2), value);
        }
    }
    output
}

pub fn read_single_data(filepath:& str) -> HashMap<String, f64> {
    let contents:&str = &read_to_string(filepath)
        .expect("Invalid filepath");

    let mut output:HashMap<String, f64> = HashMap::new();

    let lines:Vec<&str> = contents.split("\r\n").collect();

    for line in &lines[1..] {
        let words:Vec<&str> = line.split("\t").collect();
        output.insert(String::from(words[0]), words[1].parse().unwrap());
    }
    output
}

pub fn get_all_data() -> AllData {
    AllData { 
        single_key_names: vec![
            "000", "010", "020", "030", "040",
            "100", "110", "120", "130", "140",
            "200", "210", "220", "230", "240",
            "001", "011", "021", "031", "041",
            "101", "111", "121", "131", "141",
            "201", "211", "221", "231", "241",
        ],
        single_key_data: vec![
            3.73, 3.73, 3.93, 3.15, 1.76,
            5.15, 5.25, 5.35, 5.25, 4.05,
            3.32, 4.12, 4.22, 3.82, 3.15,

            3.73, 3.73, 3.93, 3.15, 1.76,
            5.15, 5.25, 5.35, 5.25, 4.05,
            3.32, 4.12, 4.22, 3.82, 3.15,
        ],
        combination_key_data: read_combination_data("data/combination_key_data.txt"),
        single_letter_data: read_single_data("data/single_letter_data.txt"),
        combination_letter_data: read_combination_data("data/combination_letter_data.txt")
    }
}