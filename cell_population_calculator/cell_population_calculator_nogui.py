# Input of starting population and days of observation
cells = int(input())
days = int(input())

# Counter for the days 
counter = 1

# Loop till every day passed
while counter <= days:
  cells = cells * 2
  print(f"Day {counter}: {cells}")
  counter = counter + 1
