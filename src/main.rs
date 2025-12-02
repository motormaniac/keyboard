use individual::Individual;
use population::Population;
use graph::{DataPoint,create_csv};

mod fileio;
mod individual;
mod population;
mod graph;

use std::fs;

// How many times to generate the next population
const GENERATIONS:usize = 80;

fn main() {
    let all_data = fileio::get_all_data();
    let mut population = Population::random_population(&all_data);
    let mut last_average_fitness = population.average_fitness;
    let mut data_points:Vec<DataPoint> = vec![DataPoint::new(&population)];
    for i in 0..GENERATIONS {
        println!("\nMaking generation: {i}");
        population = population.create_next_population(&all_data);
        data_points.push(DataPoint::new(&population));
        println!("Improvement: {:?}", population.average_fitness - last_average_fitness);
        last_average_fitness = population.average_fitness;

        let this_best_individual = population.individuals.first().unwrap();
        println!("This best layout: {:?}", this_best_individual.layout);
    }
    create_csv("layout_data/layout_data.txt", &data_points);
}
