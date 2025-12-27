import type { Label } from "../interfaces/interfacesList";

interface LabelComponentProps {
    label: Label;
}

export function LabelComponent({ label }: LabelComponentProps) {
    return(
        <div>
            <p>{label.subtitle}</p>
            <p>{label.subtitleData}</p>
        </div>
    );
}