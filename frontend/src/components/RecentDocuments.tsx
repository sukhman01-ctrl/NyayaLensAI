import React from 'react';
import { DocumentListItem } from '../types';

interface RecentDocumentsProps {
  documents: DocumentListItem[];
  onSelectDocument: (doc: DocumentListItem) => void;
  selectedDocId?: number;
}

export const RecentDocuments: React.FC<RecentDocumentsProps> = ({
  documents,
  onSelectDocument,
  selectedDocId
}) => {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'Reviewed':
        return (
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-[#0D281E] border border-emerald-500/30 text-emerald-400">
            Reviewed
          </span>
        );
      case 'Processing':
        return (
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-[#11243E] border border-blue-500/30 text-blue-400">
            Processing
          </span>
        );
      case 'Risk Found':
      default:
        return (
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-[#2F1C0B] border border-amber-500/30 text-amber-400">
            Risk Found
          </span>
        );
    }
  };

  const getFileTypeBadge = (type: string) => {
    const isDoc = type.toUpperCase().includes('DOC');
    return (
      <div
        className={`w-11 h-11 rounded-xl flex items-center justify-center font-bold text-xs uppercase tracking-wider ${
          isDoc ? 'bg-[#15284F] text-blue-300' : 'bg-[#1A2038] text-purple-300'
        }`}
      >
        {isDoc ? 'DOC' : 'PDF'}
      </div>
    );
  };

  return (
    <div className="bg-[#121929] border border-white/5 rounded-2xl p-6">
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-sm font-bold tracking-wider text-slate-400 uppercase">
          Recent Documents
        </h2>
        <span className="text-xs text-purple-400 font-medium cursor-pointer hover:underline">
          View All ({documents.length})
        </span>
      </div>

      <div className="space-y-3">
        {documents.map((doc) => {
          const isSelected = selectedDocId === doc.id;
          return (
            <div
              key={doc.id}
              onClick={() => onSelectDocument(doc)}
              className={`p-4 rounded-xl border flex items-center justify-between cursor-pointer transition-all duration-150 ${
                isSelected
                  ? 'bg-[#18233C] border-purple-500/50 shadow-md'
                  : 'bg-[#0E1524]/60 border-white/5 hover:bg-[#151F35] hover:border-white/10'
              }`}
            >
              <div className="flex items-center space-x-4">
                {getFileTypeBadge(doc.file_type)}
                <div>
                  <div className="text-sm font-semibold text-white group-hover:text-purple-300 transition-colors">
                    {doc.title}
                  </div>
                  <div className="text-xs text-slate-400 mt-1 flex items-center gap-2">
                    <span>{doc.page_count} pages</span>
                    <span>•</span>
                    <span>Uploaded recently</span>
                    <span>•</span>
                    <span className={doc.clauses_flagged > 0 ? 'text-amber-400 font-medium' : 'text-slate-400'}>
                      {doc.clauses_flagged > 0 ? `${doc.clauses_flagged} clauses flagged` : 'Clean'}
                    </span>
                  </div>
                </div>
              </div>

              <div>{getStatusBadge(doc.status)}</div>
            </div>
          );
        })}

        {documents.length === 0 && (
          <div className="py-12 text-center text-slate-500 text-sm">
            No documents uploaded yet. Upload a document to begin analysis.
          </div>
        )}
      </div>
    </div>
  );
};
