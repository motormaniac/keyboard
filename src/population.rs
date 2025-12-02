use std::io::Write;
use crate::individual::Individual;
use crate::fileio::AllData;
use rayon::prelude::*;

pub struct Population {
    pub individuals:Vec<Individual>,
    pub average_fitness:f64,
}

const POPULATION_SIZE:usize = 100000;
// top_percentile = what percent of top performers from this generation move to the next
const TOP_PERCENTILE:f64 = 0.10;
/// random_percentile = what percent of random parents to select
const RANDOM_PERCENTILE:f64 = 0.4;
// When picking a random parent, how many random things to choose from before picking the best one out of those
// MUST BE GREATER THAN 0
const RANDOM_PICK_AMOUNT:usize = 3;
/// mutate_chance = chance for an individual to mutate (switch once)
const MUTATE_CHANCE:f64 = 0.01;

//List of Individuals. Individuals are sorted in descending order (highest fitness first)
impl Population {
    pub fn random_population(all_data:&AllData) -> Self {
        println!("\nMake Random Population");
        let mut new_population = Population{
            individuals:Vec::with_capacity(POPULATION_SIZE),
            average_fitness:0f64,
        };

        let mut accumulated_score:f64 = 0f64;
        println!("Filling Population");
        for i in 0..POPULATION_SIZE {
            if i%1000 == 0 {
                let progress = (100f32 * i as f32 / POPULATION_SIZE as f32).round();
                print!("\rProgress: {progress}%");
                std::io::stdout().flush();
            }
            let new_individual = Individual::random(all_data);
            accumulated_score += new_individual.fitness;
            new_population.individuals.push(new_individual);
        };
        println!("\rProgress: 100%");
        new_population.average_fitness = accumulated_score / POPULATION_SIZE as f64;

        //sort by fitness
        new_population.individuals.sort_by(
            |a, b| a.fitness.partial_cmp(&b.fitness).unwrap());
        new_population.individuals.reverse();
        println!("Finished population. Average fitness: {:?}", new_population.average_fitness);
        new_population
    }
    // picks quantity individuals from self, and gives the best out of those
    fn pick_random_parent(&self) -> &Individual {
        let mut max_parent:Option<&Individual> = None;
        for _ in 0..RANDOM_PICK_AMOUNT {
            let current_parent = &self.individuals[rand::random_range(0..self.individuals.len())];
            match max_parent {
                None => max_parent = Some(current_parent),
                Some(x) => {
                    if current_parent.fitness > x.fitness {
                        max_parent = Some(current_parent);
                    }
                }
            };
        }
        max_parent.unwrap()
    }
    //Creates a new population derived from the old one.
    pub fn create_next_population(&self, all_data:&AllData) -> Self {
        let mut new_population:Self = Self {
            individuals: Vec::new(),
            average_fitness: 0f64,
        };

        println!("Getting Top Percentile");
        let split_index = (self.individuals.len() as f64 * TOP_PERCENTILE) as usize;
        //clone the top 10% of individuals into the new population
        new_population.individuals.extend_from_slice(&self.individuals[0..split_index]);

        println!("Choosing Parents");
        //choose parents for the crossover step
        let parent_size = (self.individuals.len() as f64 * RANDOM_PERCENTILE) as usize;
        let mut new_parents:Vec<&Individual> = Vec::new();
        for _ in 0..parent_size {
            //for each parent, pick [quantity] random individuals and pick the best
            new_parents.push(self.pick_random_parent());
        }

        println!("Applying Crossover");
        //apply crossover to consecutive pairs of parents in new_parents.
        //If all parents are exhausted, but population is not full, loop through parents again

        let num_pairs = POPULATION_SIZE - split_index / 2; // Round up for odd numbers
        let mut crossover_population: Vec<Individual> = (0..num_pairs)
            .into_par_iter()
            .flat_map(|pair_index| {
                let i = (pair_index * 2) % new_parents.len();
                let (child1, child2) = Individual::crossover(
                    new_parents[i], 
                    new_parents[i + 1], 
                    all_data
                );
                vec![child1, child2]
            })
            .collect();

        //remove excess members
        while crossover_population.len() > POPULATION_SIZE - split_index {
            crossover_population.pop();
        }

        println!("Mutating");
        //mutate crossover population
        for indiv in &mut crossover_population {
            if rand::random::<f64>() < MUTATE_CHANCE {
                indiv.switch();
            };
        }
        new_population.individuals.append(&mut crossover_population);

        //sort by fitness
        new_population.individuals.sort_by(
            |a, b| a.fitness.partial_cmp(&b.fitness).unwrap());
        new_population.individuals.reverse();

        let mut accum_fitness:f64 = 0f64;
        for indiv in &new_population.individuals {
            accum_fitness += indiv.fitness;
        }
        new_population.average_fitness = accum_fitness / POPULATION_SIZE as f64;

        println!("Finished population. Average fitness: {:?}", new_population.average_fitness);
        new_population
    }

}
