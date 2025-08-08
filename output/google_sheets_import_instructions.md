
# Google Sheets Import Instructions

## Step 1: Create New Google Sheet
1. Go to sheets.google.com
2. Click "Blank" to create a new spreadsheet
3. Name it "Underwriting Template - Pre Optimization" or "Post Optimization"

## Step 2: Import CSV Data
1. In your new Google Sheet, go to File > Import
2. Upload the CSV file from the output folder
3. Choose "Replace current sheet"
4. Click "Import data"

## Step 3: Add Formulas (Manual)
After importing, you'll need to add these formulas manually:

### Purchase Details Section:
- Down Payment: =B[Purchase Price Row]*0.2
- Loan Amount: =B[Purchase Price Row]-C[Down Payment Row]
- Monthly Payment: =PMT(0.065/12,360,C[Loan Amount Row])
- Closing Costs: =B[Purchase Price Row]*0.03
- Total OOP: =C[Down Payment Row]+C[Closing Costs Row]

### Cash Flow Analysis:
- Annual Operating Expenses: =B[Monthly Expenses Row]*12
- Net Operating Income: =B[Monthly Rent Row]-B[Monthly Expenses Row]
- Annual NOI: =C[Monthly NOI Row]*12
- Cash Flow: =B[Monthly NOI Row]-B[Monthly Payment Row]
- Annual Cash Flow: =C[Monthly Cash Flow Row]*12
- CoC Return: =C[Annual Cash Flow Row]/C[Total OOP Row]

### Return Analysis:
- Improvement: =C[Optimized Row]-B[Initial Row]

## Step 4: Formatting
1. Select header rows and apply bold formatting
2. Use conditional formatting for positive/negative values
3. Apply currency formatting to monetary values
4. Apply percentage formatting to return values

## Step 5: Share
1. Click "Share" in the top right
2. Set permissions to "Anyone with the link can view"
3. Copy the sharing link for distribution

## Step 6: Create Google Sheets Links
1. After setting up the sheet, click "Share"
2. Set permissions to "Anyone with the link can view"
3. Copy the sharing link
4. Add the link to APPLICATION.md under FINAL RESULTS
