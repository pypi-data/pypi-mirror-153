import { LayoutDOM, LayoutDOMView } from "models/layouts/layout_dom";
import * as p from "core/properties";
declare namespace NGL {
    class AtomProxy {
    }
    class Blob {
        constructor(list: Array<String>, ob: object);
    }
    class Colormaker {
        atomColor: (atom: AtomProxy) => string;
    }
    class ColormakerRegistry {
        static addScheme(scheme: () => void): String;
        static addSelectionScheme(dataList: Array<Array<String>>, label: String): String;
    }
    class Component {
        removeAllRepresentations(): void;
        addRepresentation(type: String, params?: object): RepresentationComponent;
        reprList: RepresentationElement[];
    }
    class Matrix4 {
        elements: Array<Number>;
    }
    class RepresentationComponent {
    }
    class RepresentationElement {
        setParameters(params: any): this;
        getParameters(): object;
    }
    class Stage {
        compList: Array<Component>;
        viewerControls: ViewerControls;
        constructor(elementId: String, params?: object);
        loadFile(s: String | Blob, params?: object): Promise<StructureComponent>;
        autoView(): void;
        setSpin(flag: Boolean): void;
        removeAllComponents(type: String): void;
        addRepresentation(representation: String): void;
        handleResize(): void;
    }
    class ScriptComponent {
        constructor(stage: Stage, params?: object);
        addRepresentation(type: String, params?: object): RepresentationComponent;
        autoView(): void;
        removeAllRepresentations(): void;
        reprList: RepresentationElement[];
    }
    class StructureComponent {
        constructor(stage: Stage, params?: object);
        addRepresentation(type: String, params?: object): RepresentationComponent;
        autoView(): void;
        removeAllRepresentations(): void;
        reprList: RepresentationElement[];
    }
    class SurfaceComponent {
        constructor(stage: Stage, params?: object);
        addRepresentation(type: String, params?: object): RepresentationComponent;
        autoView(): void;
        removeAllRepresentations(): void;
        reprList: RepresentationElement[];
    }
    class Vector3 {
        x: number;
        y: number;
        z: number;
    }
    class ViewerControls {
        position: Vector3;
        Orientation: Matrix4;
    }
}
export declare class NGLView extends LayoutDOMView {
    model: ngl;
    spin: Boolean;
    _stage: NGL.Stage;
    initialize(): void;
    set_variable_x(x: number): void;
    private _init;
    get child_models(): LayoutDOM[];
    _update_layout(): void;
}
export declare namespace ngl {
    type Attrs = p.AttrsOf<Props>;
    type Props = LayoutDOM.Props & {
        spin: p.Property<boolean>;
        representation: p.Property<string>;
        rcsb_id: p.Property<string>;
        color_list: p.Property<any>;
        pdb_string: p.Property<string>;
    };
}
export interface ngl extends ngl.Attrs {
}
export declare class ngl extends LayoutDOM {
    properties: ngl.Props;
    __view_type__: NGLView;
    constructor(attrs?: Partial<ngl.Attrs>);
    static __name__: string;
    static init_ngl(): void;
}
export {};
