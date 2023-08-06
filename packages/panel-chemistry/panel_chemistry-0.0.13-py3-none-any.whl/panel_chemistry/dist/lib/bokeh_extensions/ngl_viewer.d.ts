import * as p from "@bokehjs/core/properties";
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
export declare class NGLViewerView extends HTMLBoxView {
    model: NGLViewer;
    _stage: any;
    connect_signals(): void;
    render(): void;
    setBackgroundcolor(): void;
    after_layout(): void;
    updateEffect(): void;
    getParameters(): {
        color: String;
        colorScheme?: undefined;
    } | {
        colorScheme: string;
        color?: undefined;
    };
    updateParameters(): void;
    updateStage(): void;
}
export declare namespace NGLViewer {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        object: p.Property<string>;
        extension: p.Property<string>;
        representation: p.Property<string>;
        color_scheme: p.Property<string>;
        custom_color_scheme: p.Property<any>;
        effect: p.Property<string>;
    };
}
export interface NGLViewer extends NGLViewer.Attrs {
}
export declare class NGLViewer extends HTMLBox {
    properties: NGLViewer.Props;
    constructor(attrs?: Partial<NGLViewer.Attrs>);
    static __module__: string;
    static init_NGLViewer(): void;
}
