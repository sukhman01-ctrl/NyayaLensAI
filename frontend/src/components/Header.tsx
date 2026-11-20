import React from 'react';
import { Search, UploadCloud, Globe, Sparkles } from 'lucide-react';

interface HeaderProps {
  onOpenUpload: () => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  language: string;
  onLanguageChange: (lang: string) => void;
}

export const Header: React.FC<HeaderProps> = ({
  onOpenUpload,
  searchQuery,
  onSearchChange,
  language,
  onLanguageChange
}) => {
  return (
    <header className="h-20 border-b border-white/5 px-8 flex items-center justify-between bg-[#0B0F19]/80 backdrop-blur sticky top-0 z-20">
      {/* Title & Status Pill matching reference screenshot */}
      <div className="flex items-center space-x-4">
        <h1 className="text-2xl font-bold tracking-tight text-white">Document Intelligence</h1>
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-[#18223B] border border-blue-500/20 text-xs font-semibold text-blue-300 shadow-sm">
          <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
          <span>AI Processing Active</span>
        </div>
      </div>

      {/* Right Controls: Search, Language Switcher, Upload Button */}
      <div className="flex items-center space-x-4">
        {/* Search Input matching reference screenshot */}
        <div className="relative w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search documents..."
            className="w-full bg-[#131A2B] border border-white/10 rounded-xl pl-10 pr-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-purple-500/50 transition-colors"
          />
        </div>

        {/* Multilingual Selector */}
        <div className="flex items-center bg-[#131A2B] border border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-slate-300">
          <Globe className="w-3.5 h-3.5 text-purple-400 mr-1.5" />
          <select
            value={language}
            onChange={(e) => onLanguageChange(e.target.value)}
            className="bg-transparent focus:outline-none cursor-pointer font-medium text-slate-200"
          >
            <option value="en" className="bg-[#131A2B] text-white">English</option>
            <option value="hi" className="bg-[#131A2B] text-white">हिन्दी (Hindi)</option>
            <option value="pa" className="bg-[#131A2B] text-white">ਪੰਜਾਬੀ (Punjabi)</option>
          </select>
        </div>

        {/* Upload Button */}
        <button
          onClick={onOpenUpload}
          className="flex items-center space-x-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium px-4 py-2 rounded-xl text-sm transition-all duration-150 shadow-lg shadow-purple-600/20 active:scale-95"
        >
          <UploadCloud className="w-4 h-4" />
          <span>Upload Document</span>
        </button>
      </div>
    </header>
  );
};
