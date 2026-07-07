import re

with open('src/pages/ConferenceTableCalculator.tsx', 'r') as f:
    content = f.read()

# I see the issue. The calculateCost function is declared OUTSIDE the component (or the useMemo is capturing things incorrectly). Let's check where the cost calculation happens.
