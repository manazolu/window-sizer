Code Organization:
- [x] Consider splitting calculations into a separate calculations.py module - the main file has grown quite large
- [x] Move table column definitions to a config section or separate file

Error Handling:
- Add validation for edge cases (zero/negative dimensions)
- Handle WeasyPrint system dependency errors more gracefully
- Consider input sanitization beyond basic digit validation

User Experience:
- Add keyboard shortcuts (Enter to submit form)
- Consider adding undo functionality for row deletions
- Show calculation preview before adding to table

Code Quality:
- The delete_row function exists but isn't used - remove or wire up to individual row delete buttons
- Consider using Enums for RAM types instead of string literals
- Add type hints throughout for better maintainability

Performance:
- For large tables, consider pagination or virtual scrolling
- Cache PDF template compilation

Features:
- Add export to CSV/Excel alongside PDF
- Consider saving/loading table data
- Add print settings (page orientation, margins)

Testing:
- Add unit tests for calculation functions
- Consider integration tests for the UI workflow