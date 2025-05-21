The project outlined, Data-Privacy-Guard, aims to identify and mask sensitive data within datasets. This can help in ensuring compliance with data privacy regulations such as GDPR and CCPA. Below is a complete Python program that demonstrates how one might achieve such functionality. For simplicity, we will focus on using a CSV dataset and will employ basic techniques using regular expressions to identify predictable sensitive fields like emails and phone numbers. We'll mask these fields for privacy.

```python
import pandas as pd
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    """Load data from a CSV file into a Pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        logging.info("Data loaded successfully")
        return data
    except FileNotFoundError:
        logging.error("File not found. Please provide a valid file path.")
    except pd.errors.EmptyDataError:
        logging.error("No data found. The file is empty.")
    except Exception as e:
        logging.error(f"An error occurred while loading data: {e}")

def detect_sensitive_data(data):
    """Identify potential sensitive data such as emails and phone numbers."""
    sensitive_data_patterns = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b'
    }
    
    sensitive_columns = []
    for col in data.columns:
        for pattern_name, pattern in sensitive_data_patterns.items():
            if data[col].astype(str).str.contains(pattern, regex=True, na=False).any():
                logging.info(f"Sensitive data detected: {pattern_name} in column {col}")
                sensitive_columns.append(col)
                break  # Move to next column if pattern found
    return sensitive_columns

def mask_sensitive_data(data, sensitive_columns):
    """Mask the data in the specified columns."""
    def mask_email(email):
        username, domain = email.split('@')
        masked_username = username[:1] + '*****' if len(username) > 1 else '*****'
        return masked_username + '@' + domain
    
    def mask_phone(phone):
        return '***-***-' + phone[-4:]

    for col in sensitive_columns:
        if 'email' in col:
            data[col] = data[col].apply(lambda x: mask_email(x) if pd.notnull(x) else x)
        elif 'phone' in col:
            data[col] = data[col].apply(lambda x: mask_phone(x) if pd.notnull(x) else x)
        logging.info(f"Data in column {col} has been masked.")
    
    return data

def save_data(data, output_path):
    """Save the masked DataFrame to a new CSV file."""
    try:
        data.to_csv(output_path, index=False)
        logging.info(f"Masked data saved to {output_path}")
    except Exception as e:
        logging.error(f"An error occurred while saving data: {e}")

        
def main():
    # Replace 'your_dataset.csv' with your file path
    file_path = 'your_dataset.csv'
    output_path = 'masked_data.csv'

    # Load data
    data = load_data(file_path)
    if data is None:
        return

    # Detect sensitive data
    sensitive_columns = detect_sensitive_data(data)

    # Mask sensitive data
    masked_data = mask_sensitive_data(data, sensitive_columns)

    # Save masked data
    save_data(masked_data, output_path)


if __name__ == '__main__':
    main()
```

### Key Points:
- **Logging and Error Handling**: The program uses the `logging` module for tracking the application flow and handling errors effectively. Error messages are logged, which can be useful for debugging.
- **Pattern Matching**: Regular expressions (regex) are used to identify common patterns of sensitive data, such as emails and phone numbers.
- **Masking**: The program masks detected sensitive information, ensuring data privacy.
- **Pandas**: The Python library Pandas is used for data manipulation, which efficiently handles large datasets.

This script provides a basic framework and can be built upon for more sophisticated needs, including additional types of sensitive data, more complex masking techniques, and enhanced compliance features.