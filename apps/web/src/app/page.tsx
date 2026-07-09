'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import UploadZone from '@/components/UploadZone';
import VideoPreview from '@/components/VideoPreview';
import LoadingOverlay from '@/components/LoadingOverlay';
import CaptionCard from '@/components/CaptionCard';
import ExportBar from '@/components/ExportBar';
import { useFileUpload } from '@/hooks/useFileUpload';
import { useCaptionGeneration } from '@/hooks/useCaptionGeneration';
import { CAPTION_STYLES, CaptionStyle } from '@/types/caption';
import { exportTxt, exportVideo } from '@/services/api';
import { downloadBlob } from '@/utils/download';

export default function Home() {
  const { file, previewUrl, error: fileError, handleFile, clearFile } = useFileUpload();
  const { status, loadingMessage, captions, error: genError, generate, reset } = useCaptionGeneration();
  
  // Track user edits to captions
  const [editedCaptions, setEditedCaptions] = useState<Record<string, string>>({});

  const handleUpdateCaption = (style: CaptionStyle, text: string) => {
    setEditedCaptions((prev) => ({ ...prev, [style]: text }));
  };

  const handleClear = () => {
    clearFile();
    reset();
    setEditedCaptions({});
  };

  const handleExportTxt = async () => {
    if (!captions) return;
    // Merge original captions with any edits
    const finalCaptions = { ...captions, ...editedCaptions };
    const blob = await exportTxt(finalCaptions);
    downloadBlob(blob, 'describex_captions.txt');
  };

  const handleExportVideo = async () => {
    if (!file || !captions) return;
    
    // We'll burn the formal caption by default, or you can allow selection.
    // The prompt says "Burn captions" but usually you pick one style.
    // We'll use the Formal style by default if they don't specify, 
    // or we can just burn the formal style for this MVP.
    const finalCaptions = { ...captions, ...editedCaptions };
    const textToBurn = finalCaptions.formal;
    
    const blob = await exportVideo(file, textToBurn);
    downloadBlob(blob, `captioned_${file.name}`);
  };

  return (
    <div className="min-h-screen bg-black text-zinc-300 font-sans selection:bg-zinc-800">
      <Header />
      
      <main className="max-w-[1280px] mx-auto px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          
          {/* Left Column: Video & Controls */}
          <div className="lg:col-span-5 space-y-8">
            <div className="space-y-4">
              <h2 className="text-3xl font-semibold text-white tracking-tight">Generate Captions</h2>
              <p className="text-zinc-400">
                Upload your video to automatically generate four expressive caption styles using Fireworks AI.
              </p>
            </div>

            {fileError && (
              <div className="p-4 bg-red-950/50 border border-red-900 rounded-lg text-red-200 text-sm">
                {fileError}
              </div>
            )}
            
            {genError && (
              <div className="p-4 bg-red-950/50 border border-red-900 rounded-lg text-red-200 text-sm">
                {genError}
              </div>
            )}

            {!previewUrl ? (
              <UploadZone onFileSelect={handleFile} />
            ) : (
              <VideoPreview 
                url={previewUrl} 
                filename={file?.name || ''} 
                onClear={handleClear} 
              />
            )}

            {previewUrl && status === 'idle' && (
              <button
                onClick={() => generate(file!)}
                className="w-full py-4 bg-white text-black font-semibold rounded-xl text-lg hover:bg-zinc-200 transition-colors shadow-lg shadow-white/5"
              >
                Generate Captions
              </button>
            )}
          </div>

          {/* Right Column: Output */}
          <div className="lg:col-span-7">
            {status === 'idle' && (
              <div className="h-full min-h-[400px] border border-dashed border-zinc-800 rounded-xl flex items-center justify-center text-zinc-600 bg-zinc-900/20">
                <p>Captions will appear here after generation</p>
              </div>
            )}

            {status === 'processing' && (
              <div className="h-full min-h-[400px] flex items-center justify-center">
                <LoadingOverlay message={loadingMessage} />
              </div>
            )}

            {status === 'done' && captions && (
              <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-white">Generated Captions</h3>
                  <p className="text-sm text-zinc-400">Review and edit your captions below before exporting.</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {CAPTION_STYLES.map((style) => (
                    <CaptionCard
                      key={style}
                      styleName={style}
                      initialText={captions[style]}
                      onUpdate={handleUpdateCaption}
                    />
                  ))}
                </div>

                <ExportBar 
                  onExportTxt={handleExportTxt}
                  onExportVideo={handleExportVideo}
                />
              </div>
            )}
          </div>

        </div>
      </main>

      <Footer />
    </div>
  );
}
