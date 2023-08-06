import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export declare class JSMEEditorView extends HTMLBoxView {
    model: JSMEEditor;
    jsmeElement: any;
    JSME: any;
    valueFunc: any;
    valueChanging: boolean;
    connect_signals(): void;
    render(): void;
    setGUIColor(): void;
    setJSMEOptions(): void;
    getHeight(): string;
    getWidth(): string;
    resizeJSMEElement(): void;
    after_layout(): void;
}
export declare namespace JSMEEditor {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        value: p.Property<string>;
        format: p.Property<string>;
        options: p.Property<string[]>;
        jme: p.Property<string>;
        smiles: p.Property<string>;
        mol: p.Property<string>;
        mol3000: p.Property<string>;
        sdf: p.Property<string>;
        subscriptions: p.Property<string[]>;
        guicolor: p.Property<string>;
    };
}
export interface JSMEEditor extends JSMEEditor.Attrs {
}
export declare class JSMEEditor extends HTMLBox {
    properties: JSMEEditor.Props;
    constructor(attrs?: Partial<JSMEEditor.Attrs>);
    static __module__: string;
    static init_JSMEEditor(): void;
}
