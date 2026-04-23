import React, { useState } from 'react';

export default function UploadPDF({ onUpload }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    await onUpload(file);
    setUploading(false);
    setFile(null);
  };
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <h3 className="font-semibold text-gray-800 mb-3">Upload Finqalab PDF</h3>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} className="text-sm" />
        <button type="submit" disabled={!file || uploading} className="bg-primary text-white px-4 py-2 rounded-lg text-sm font-medium disabled:opacity-50">
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
}