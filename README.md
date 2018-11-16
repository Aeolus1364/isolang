# isolang

This project started as a programming language for a life simulation game. 
I have moved it to its own repository to focus more on its development. 

There are a few rules for this language:

1. Code is split up into terms with one being evaluated per step

2. Commands and arguments are interchangeable, allowing infinite hierarchy

3. Commands have access to the stream of terms, allowing self modification

4. There is no difference between a term you type and a value being returned

5. The newest command has the highest priority and receives all arguments until it resolves

6. Commands collapse on resolution
