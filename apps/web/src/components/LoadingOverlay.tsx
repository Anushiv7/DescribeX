'use client';

interface LoadingOverlayProps {
  message: string;
}

const PIPELINE_STEPS = [
  'Uploading video...',
  'Extracting frames...',
  'Analyzing scene...',
  'Generating caption styles...',
  'Almost done...',
];

export default function LoadingOverlay({ message }: LoadingOverlayProps) {
  const currentIndex = PIPELINE_STEPS.indexOf(message);

  return (
    <div className="flex flex-col items-center justify-center p-12 bg-zinc-900/40 border border-zinc-800 rounded-3xl backdrop-blur-md shadow-2xl w-full max-w-md mx-auto">
      <div className="w-12 h-12 border-[3px] border-zinc-700 border-t-[#ED1C24] rounded-full animate-spin mb-8"></div>
      
      <div className="w-full space-y-4">
        {PIPELINE_STEPS.map((step, index) => {
          const isCompleted = currentIndex > index;
          const isActive = currentIndex === index;
          
          return (
            <div 
              key={step} 
              className={`flex items-center gap-4 transition-all duration-300 ${
                isActive ? 'opacity-100 scale-105 transform translate-x-2' : 
                isCompleted ? 'opacity-50' : 'opacity-30'
              }`}
            >
              <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 transition-colors ${
                isCompleted ? 'bg-[#ED1C24] text-white' : 
                isActive ? 'border-2 border-[#ED1C24]' : 'border-2 border-zinc-700'
              }`}>
                {isCompleted && (
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                )}
                {isActive && <div className="w-2.5 h-2.5 bg-[#ED1C24] rounded-full animate-pulse"></div>}
              </div>
              <span className={`font-medium ${isActive ? 'text-white tracking-tight' : 'text-zinc-400'}`}>
                {step}
              </span>
            </div>
          );
        })}
      </div>
      
      <p className="text-zinc-500 text-sm mt-10 font-medium">This process usually takes 1-2 minutes.</p>
    </div>
  );
}
