import type { Label } from "../interfaces/interfacesList";

interface LabelComponentProps {
    label: {
        subtitle: string;
        subtitleData: React.ReactNode;
    }
}

export function LabelComponent({ label }: LabelComponentProps) {
    return(
        <div className='p-2'>
            <span className='text-xs text-gray-400 font-semibold p-1'>{label.subtitle}</span>
            <p className='text-lg text-black font-bold p-1'>{label.subtitleData}</p>
        </div>
    );
}