export type LabelSubtitle = 'drone id' | 'latitude' | 'longitude' | 'altitude' | 'radar id' | 'radar range' | 'radar' | 'distance'
export type LabelSize = 'small' | 'medium' | 'large'

export interface Label {
    icon: string;
    subtitle: LabelSubtitle;
    subtitleSize?: LabelSize;
    subtitleData: string;
}

