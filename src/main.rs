use individual::Individual;
use population::Population;

mod fileio;
mod individual;
mod population;

use std::fs;

// How many times to generate the next population
const GENERATIONS:usize = 100;

fn main() {
    let all_data = fileio::get_all_data();
    // let indiv = Individual::from_layout(
    //     vec![
    //         "SPACE","A","B","C","D",
    //         "E","F","G","H","I",
    //         "J","K","L","M","N",
    //         "SPACE","O","P","Q","R",
    //         "S","T","U","V","W",
    //         "X","Y","Z","_","_"], 
    //     &all_data
    // );
    // println!("{:?}", indiv.fitness);
    let mut population = Population::random_population(&all_data);
    let mut last_average_fitness = population.average_fitness;
    for i in 0..GENERATIONS {
        println!("\nMaking generation: {i}");
        population = population.create_next_population(&all_data);
        println!("Improvement: {:?}", population.average_fitness - last_average_fitness);
        last_average_fitness = population.average_fitness;

        let this_best_individual = population.individuals.last().unwrap();
        println!("This best layout: {:?}", this_best_individual.layout);
    }
    let best_individual = population.individuals.last().unwrap();
}
