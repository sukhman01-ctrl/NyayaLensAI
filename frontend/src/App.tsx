import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { MetricCards } from './components/MetricCards';
import { RecentDocuments } from './components/RecentDocuments';
import { AiInsightsStream } from './components/AiInsightsStream';
import { DocumentWorkspace } from './components/DocumentWorkspace';
import { UploadModal } from './components/UploadModal';
import { ComparisonModal } from './components/ComparisonModal';
import { 
  DocumentListItem, 
  DocumentDetail, 
  DashboardKPIs, 
  AIInsightItem 
} from './types';
import { 
  fetchDocuments, 
  fetchDocumentDetail, 
  fetchDashboardKPIs, 
  fetchAIInsights 
} from './services/api';

export function App() {
  const [currentView, setCurrentView] = useState('documents');
  const [documents, setDocuments] = useState<DocumentListItem[]>([]);
  const [kpis, setKpis] = useState<DashboardKPIs | null>(null);
  const [insights, setInsights] = useState<AIInsightItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [language, setLanguage] = useState('en');

  // Modals & Workspace State
  const [selectedDoc, setSelectedDoc] = useState<DocumentDetail | null>(null);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [isComparisonOpen, setIsComparisonOpen] = useState(false);

  useEffect(() => {
    async function initData() {
      try {
        const [docsData, kpiData, insightsData] = await Promise.all([
          fetchDocuments(),
          fetchDashboardKPIs(),
          fetchAIInsights()
        ]);
        setDocuments(docsData);
        setKpis(kpiData);
        setInsights(insightsData);
      } catch (err) {
        console.error('Error fetching initial dashboard data', err);
      }
    }
    initData();
  }, []);

  const handleSelectDocument = async (doc: DocumentListItem) => {
    try {
      const fullDoc = await fetchDocumentDetail(doc.id);
      setSelectedDoc(fullDoc);
    } catch (e) {
      console.error(e);
    }
  };

  const handleNavSelect = (view: string) => {
    setCurrentView(view);
    if (view === 'comparison') {
      setIsComparisonOpen(true);
    } else if (view === 'contract_review' || view === 'risk_analysis' || view === 'clause_extraction' || view === 'compliance' || view === 'assistant') {
      if (documents.length > 0) {
        handleSelectDocument(documents[0]);
      }
    }
  };

  const filteredDocs = documents.filter((d) =>
    d.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.doc_type.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex min-h-screen bg-[#0B0F19] text-[#F8FAFC]">
      {/* LEFT SIDEBAR matching reference screenshot */}
      <Sidebar
        currentView={currentView}
        onSelectView={handleNavSelect}
      />

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          onOpenUpload={() => setIsUploadOpen(true)}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          language={language}
          onLanguageChange={setLanguage}
        />

        <main className="p-8 max-w-7xl mx-auto w-full">
          {/* Top KPI Metrics Cards matching reference screenshot */}
          <MetricCards kpis={kpis} />

          {/* Main Split Grid matching reference screenshot */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left 2 Cols: RECENT DOCUMENTS */}
            <div className="lg:col-span-2">
              <RecentDocuments
                documents={filteredDocs}
                onSelectDocument={handleSelectDocument}
                selectedDocId={selectedDoc?.id}
              />
            </div>

            {/* Right 1 Col: AI INSIGHTS STREAM */}
            <div className="lg:col-span-1">
              <AiInsightsStream
                insights={insights}
                onInsightClick={() => {
                  if (documents.length > 0) handleSelectDocument(documents[0]);
                }}
              />
            </div>
          </div>
        </main>
      </div>

      {/* TWO-PANEL INTERACTIVE WORKSPACE MODAL */}
      {selectedDoc && (
        <DocumentWorkspace
          document={selectedDoc}
          onClose={() => setSelectedDoc(null)}
          language={language}
        />
      )}

      {/* UPLOAD MODAL */}
      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onSuccess={(newDoc) => {
          setSelectedDoc(newDoc);
          fetchDocuments().then(setDocuments);
        }}
      />

      {/* CROSS-DOCUMENT COMPARISON MODAL */}
      <ComparisonModal
        isOpen={isComparisonOpen}
        onClose={() => setIsComparisonOpen(false)}
        documents={documents}
      />
    </div>
  );
}

export default App;
