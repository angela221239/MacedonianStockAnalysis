# Design Pattern Explanation

## Chosen Pattern: Factory Pattern

### Reason for Choosing Factory Pattern
1. **Code Modularity**: Centralizes the creation of key components like technical analysis, sentiment analysis, and LSTM models.
2. **Reusability**: Allows different parts of the application to use these components without duplicating code.
3. **Scalability**: Makes it easier to extend the application by adding new types of analyses or models.

### Implementation Details
- A `factory.py` module was added to handle the creation of objects.
- The `app.py` file was updated to use the factory methods, reducing redundancy and improving clarity.
- This pattern helps the application follow the **Single Responsibility Principle**.
