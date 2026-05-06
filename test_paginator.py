from django.core.paginator import Paginator

# Sample data
data = list(range(1, 21))  # 20 items

# Create a Paginator object
paginator = Paginator(data, 5)  # 5 items per page

# Iterate over the pages using the __iter__ method
for page in paginator:
    print([item for item in page])

print("Script completed successfully, no errors.")
