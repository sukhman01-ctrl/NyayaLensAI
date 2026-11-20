import React, { useState } from 'react';
import { UploadCloud, X, FileText, CheckCircle2 } from 'lucide-react';
import { uploadDocument } from '../services/api';
import { DocumentDetail } from '../types';

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (newDoc: DocumentDetail) => void;
}

export const UploadModal: React.FC<UploadModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      setFile(selected);
      if (!title) {
        setTitle(selected.name.replace(/\.[^/.]+$/, ''));
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF, DOCX, or TXT file.');
      return;
    }
    setIsUploading(true);
    setError(null);

    try {
      const doc = await uploadDocument(file, title);
      onSuccess(doc);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Error uploading document.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#121929] border border-white/10 rounded-2xl w-full max-w-lg p-6 relative shadow-2xl">
        <button
          onClick={onClose}
          className="absolute right-5 top-5 p-1 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
            <UploadCloud className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Upload Legal Document</h3>
            <p className="text-xs text-slate-400">Supported formats: PDF, DOCX, and TXT files</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-2">
              Document Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Master Service Agreement 2026"
              className="w-full bg-[#0E1524] border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-purple-500/50"
            />
          </div>

          <div className="border-2 border-dashed border-white/15 hover:border-purple-500/50 rounded-2xl p-6 text-center cursor-pointer bg-[#0D1422] transition-colors">
            <input
              type="file"
              id="file-upload"
              accept=".pdf,.docx,.doc,.txt"
              onChange={handleFileChange}
              className="hidden"
            />
            <label htmlFor="file-upload" className="cursor-pointer block">
              <UploadCloud className="w-10 h-10 text-purple-400 mx-auto mb-2" />
              <div className="text-sm font-semibold text-slate-200">
                {file ? file.name : 'Click to select or drag and drop document'}
              </div>
              <div className="text-xs text-slate-500 mt-1">
                Preserves page mapping, clause numbers, and entity boundaries
              </div>
            </label>
          </div>

          {error && (
            <div className="p-3 rounded-xl bg-red-950/60 border border-red-500/30 text-xs text-red-300">
              {error}
            </div>
          )}

          <div className="flex justify-end space-x-3 pt-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-400 hover:text-white transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isUploading}
              className="px-5 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold text-sm transition-all shadow-lg shadow-purple-600/20 disabled:opacity-50"
            >
              {isUploading ? 'Analyzing Clauses...' : 'Ingest & Analyze'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
