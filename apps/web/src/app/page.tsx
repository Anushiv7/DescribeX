'use client';

import Image from 'next/image';
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

const PIPELINE = [
  { key: 'upload', label: 'Upload' },
  { key: 'validate', label: 'Validate' },
  { key: 'frames', label: 'Extract Frames' },
  { key: 'vision', label: 'Vision AI' },
  { key: 'caption', label: 'Caption AI' },
  { key: 'ready', label: 'Ready' },
] as const;

export default function Home() {
  const { file, previewUrl, error: fileError, handleFile, clearFile } = useFileUpload();
  const { status, loadingMessage, captions, error: genError, generate, reset } = useCaptionGeneration();

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
    const finalCaptions = { ...captions, ...editedCaptions };
    const blob = await exportTxt(finalCaptions);
    downloadBlob(blob, 'describex_captions.txt');
  };

  const handleExportVideo = async () => {
    if (!file || !captions) return;
    const finalCaptions = { ...captions, ...editedCaptions };
    const blob = await exportVideo(file, finalCaptions.formal);
    downloadBlob(blob, `captioned_${file.name}`);
  };

  const isLanding = !previewUrl;

  return (
    <div className="min-h-screen flex flex-col">
      <Header variant={isLanding ? 'minimal' : 'default'} />

      <main className="flex-1 w-full">
        {/* LANDING */}
        {isLanding && (
          <section className="max-w-3xl mx-auto px-6 pt-24 pb-32 flex flex-col items-center text-center">
            <Image
              src="/describex-logo-without_bg.png"
              alt="DescribeX"
              width={104}
              height={104}
              priority
              className="mb-10 object-contain"
            />
            <h1 className="text-6xl sm:text-7xl font-semibold tracking-[-0.04em] text-[var(--color-fg)]">
              DescribeX
            </h1>
            <p className="mt-5 text-lg text-[#B5B5B5] tracking-tight">
              AI-Powered Accessible Video Captioning
            </p>
            <p className="mt-10 text-2xl sm:text-3xl font-medium tracking-[-0.02em] text-[var(--color-fg)]">
              Create Once. <span className="text-[var(--color-muted)]">Caption Everywhere.</span>
            </p>
            <p className="mt-6 max-w-xl text-[15px] leading-relaxed text-[var(--color-muted)]">
              Upload a short video and instantly generate four AI-powered caption styles with editable
              exports and burned-in captions.
            </p>

            <div className="mt-14 w-full max-w-xl">
              {fileError && (
                <div className="mb-4 p-3 rounded-lg border border-[var(--color-accent)]/40 bg-[var(--color-accent)]/5 text-sm text-[var(--color-fg)]">
                  {fileError}
                </div>
              )}
              <UploadZone onFileSelect={handleFile} />
            </div>
          </section>
        )}

        {/* DASHBOARD */}
        {!isLanding && (
          <section className="max-w-[1240px] mx-auto px-6 py-12 space-y-10">
            {(fileError || genError) && (
              <div className="p-4 rounded-xl border border-[var(--color-accent)]/40 bg-[var(--color-accent)]/5 text-sm text-[var(--color-fg)]">
                {fileError || genError}
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-8">
              <div className="space-y-6">
                <VideoPreview
                  url={previewUrl!}
                  filename={file?.name || ''}
                  onClear={handleClear}
                />

                {status === 'idle' && (
                  <button
                    onClick={() => generate(file!)}
                    className="w-full py-4 rounded-2xl text-base font-semibold bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-white transition-all duration-200 ease-out shadow-[0_10px_40px_-10px_rgba(202,5,5,0.25)]"
                  >
                    Generate Captions
                  </button>
                )}
              </div>

              <aside className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-sm font-semibold tracking-tight text-[var(--color-fg)]">Pipeline Status</h3>
                  <span className="text-[11px] uppercase tracking-widest text-[var(--color-muted)]">
                    {status === 'processing' ? 'Running' : status === 'done' ? 'Complete' : 'Idle'}
                  </span>
                </div>

                {status === 'processing' ? (
                  <LoadingOverlay message={loadingMessage} />
                ) : (
                  <ol className="space-y-3">
                    {PIPELINE.map((step) => {
                      const complete = status === 'done';
                      return (
                        <li key={step.key} className="flex items-center gap-3 text-sm">
                          <span
                            className={`w-5 h-5 rounded-full flex items-center justify-center border ${
                              complete
                                ? 'bg-[var(--color-accent)] border-[var(--color-accent)] text-white'
                                : 'border-[var(--color-border)] text-transparent'
                            }`}
                          >
                            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3}>
                              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                            </svg>
                          </span>
                          <span className={complete ? 'text-[var(--color-fg)]' : 'text-[var(--color-muted)]'}>
                            {step.label}
                          </span>
                        </li>
                      );
                    })}
                  </ol>
                )}
              </aside>
            </div>

            {status === 'done' && captions && (
              <div className="space-y-10 pt-4">
                <div>
                  <h2 className="text-2xl font-semibold tracking-tight text-[var(--color-fg)]">Generated Captions</h2>
                  <p className="mt-2 text-sm text-[var(--color-muted)]">
                    Review and edit any style before exporting.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  {CAPTION_STYLES.map((style) => (
                    <CaptionCard
                      key={style}
                      styleName={style}
                      initialText={captions[style]}
                      onUpdate={handleUpdateCaption}
                    />
                  ))}
                </div>

                <ExportBar onExportTxt={handleExportTxt} onExportVideo={handleExportVideo} />
              </div>
            )}
          </section>
        )}
      </main>

      <Footer />
    </div>
  );
}
