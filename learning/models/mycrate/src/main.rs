use std::process::{Command};

fn main() {
	let output = Command::new("python")
						.arg("incl/test.py 65432 anger")
                     	.output()
                     	.expect("Failed to execute command");

    println!("{}", std::str::from_utf8(output.stdout.as_slice()).unwrap());
}
