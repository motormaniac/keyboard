use std::fs::read_to_string;
use std::collections::HashMap;

pub fn read_data(filepath:& str, mut input_map:HashMap<String, HashMap<String, Option<f64>>>) -> HashMap<String, HashMap<String, Option<f64>>> {
    let contents:&str = &read_to_string(filepath)
        .expect("Invalid filepath");

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

            let mut submap:HashMap<String, Option<f64>> = HashMap::new();
            submap.insert(String::from(key2), value);
            input_map.insert(String::from(key1), submap);
        }
    }
    input_map
}