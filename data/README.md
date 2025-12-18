# Data Folder

This folder contains PDF documents about non-communicable diseases that are used to build the knowledge base for the RAG chatbot.

## Current Documents

The following PDF files are currently in this folder and will be processed:

- Bladder Cancer
- Breast Cancer  
- Cancer research and development
- Cancer overview
- Cholesterol
- Colorectal Cancer
- Diabetes
- High Blood Pressure
- Liver Cancer
- Lung Cancer
- National Cancer Control Programmes
- Obesity
- Overview of Non-Communicable Diseases
- Prostate Cancer
- Skin Cancers
- Thyroid Cancer

## Adding New Documents

To add more documents to the knowledge base:

1. **Add PDF files** to this folder
2. **Re-run the setup** to process new documents:
   ```bash
   # Activate virtual environment first
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   
   python -m src.setup
   ```
3. **Restart the backend server** for changes to take effect

## Supported Formats

Currently, the system supports:
- **PDF files** (.pdf) - Primary format
- **Text files** (.txt) - Plain text documents

## Best Practices

- ✅ Use descriptive filenames (they appear in source citations)
- ✅ Ensure PDFs are text-based (not scanned images)
- ✅ Keep documents focused on NCDs and health topics
- ✅ Remove duplicates before processing
- ⚠️ Large files (>50MB) may take longer to process

## File Naming

Good examples:
- `diabetes_type2_treatment.pdf`
- `heart_disease_prevention.pdf`
- `cancer_screening_guidelines.pdf`

Avoid:
- `doc1.pdf`
- `untitled.pdf`
- `scan_20231215.pdf`

## Processing Details

When you run `python -m src.setup`, the system will:
1. Load all PDF files from this folder
2. Extract text content from each page
3. Split text into chunks (~1000 characters)
4. Create vector embeddings for each chunk
5. Store embeddings in ChromaDB (`chroma_db/` folder)

## Troubleshooting

**Error: No documents found**
- Ensure PDF files are directly in this folder (not subfolders)

**Error: Failed to extract text**
- PDF might be image-based - try converting to text-based PDF
- File might be corrupted - try opening in a PDF reader first

**Documents not showing in responses**
- Re-run `python -m src.setup` after adding new files
- Check file names don't have special characters
- Verify PDFs contain readable text

## Storage

The vector database (ChromaDB) is stored separately in the `chroma_db/` folder and does not need to be committed to version control.
