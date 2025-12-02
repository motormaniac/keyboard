use std::{fmt::format, fs};

use crate::population::Population;

pub struct DataPoint {
    layout:String,
    average_fitness:f64,
    top_percent_average_fitness:f64,
    best_fitness:f64,
}

impl DataPoint {
    pub fn new(population:&Population) -> Self {
        let mut accum_fitness:f64 = 0f64;
        let split_index = (population.individuals.len() as f64 * 0.1f64) as usize;
        //clone the top 10% of individuals into the new population
        for indiv in &population.individuals[0..split_index] {
            accum_fitness += indiv.fitness;
        }
        let best_individual = population.individuals.first().unwrap();
        let datapoint = DataPoint {
            layout:best_individual.layout.join(" "),
            best_fitness:best_individual.fitness,
            average_fitness:population.average_fitness,
            top_percent_average_fitness:accum_fitness/split_index as f64,
        };
        datapoint
    }
}

pub fn create_csv(filepath:&str, data_points:&Vec<DataPoint>) {
    let mut content:String = format!("layout\taverage fitness\ttop percent average fitness\tbest fitness");
    for point in data_points {
        content = format!("{}\r\n{}\t{}\t{}\t{}",
            content,
            point.layout, 
            point.average_fitness, 
            point.top_percent_average_fitness, 
            point.best_fitness);
    }
    fs::write(filepath, content);
}