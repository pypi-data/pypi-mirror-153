import { LayoutDOM, LayoutDOMView } from "models/layouts/layout_dom";
import { LayoutItem } from "core/layout";
export class NGLView extends LayoutDOMView {
    initialize() {
        super.initialize();
        const url = "https://cdn.jsdelivr.net/gh/arose/ngl@v2.0.0-dev.37/dist/ngl.js";
        const script = document.createElement("script");
        script.onload = () => this._init();
        script.async = false;
        script.src = url;
        document.head.appendChild(script);
    }
    set_variable_x(x) {
        this._stage.viewerControls.position.x = x;
    }
    _init() {
        //assign NGL viewer to the div of this class
        this.el.setAttribute('id', 'viewport');
        this._stage = new NGL.Stage('viewport');
        var m = this.model;
        var stage = this._stage;
        //initialize class with first values
        stage.loadFile(new Blob([m.pdb_string], { type: 'text/plain' }), { ext: 'pdb' }).then(function (o) {
            o.addRepresentation(m.representation, { color: scheme });
            o.autoView();
        });
        var scheme = NGL.ColormakerRegistry.addSelectionScheme(m.color_list, "new scheme");
        stage.setSpin(m.spin);
        window.addEventListener("resize", function () {
            stage.handleResize();
        }, false);
        //This section initiates the possible events that can be launched from the python side.
        //Each event has the name of an exported variable and should be launched whenever one
        //of these variables changes its value.
        //the spin event sets the spin to the current model.spin variable
        document.addEventListener('spin', function () {
            stage.setSpin(m.spin);
        });
        //the representation event removes the previous representation of the figure and adds the new representation in
        //model.representation
        document.addEventListener('representation', function () {
            stage.compList[0].removeAllRepresentations();
            stage.compList[0].addRepresentation(m.representation, { color: scheme });
        });
        //the rcsb_id event removes the current and loads a rcsb_id into the ngl_viewer
        document.addEventListener('rcsb_id', function () {
            stage.removeAllComponents("");
            stage.loadFile(m.rcsb_id).then(function (o) {
                o.addRepresentation(m.representation, { color: scheme });
                o.autoView();
            });
        });
        //the color_list event tries to update the colorlist of the current model, but if the list is badly defined,
        //the current colorscheme will persist. Note that the color_list is passed as an Any object, so it should first
        //be converted to an Array<Array<String>>
        document.addEventListener('color_list', function () {
            var list = m.color_list;
            try {
                scheme = NGL.ColormakerRegistry.addSelectionScheme(list, "new scheme");
                stage.compList[0].reprList[0].setParameters({ color: scheme });
            }
            catch (err) {
                console.log("badly defined color");
            }
        });
        //the pdb_string event removes the last model and loads in the new model from the pdb string
        document.addEventListener('pdb_string', function () {
            stage.removeAllComponents("");
            stage.loadFile(new Blob([m.pdb_string], { type: 'text/plain' }), { ext: 'pdb' }).then(function (o) {
                o.addRepresentation(m.representation, { color: scheme });
                o.autoView();
            });
        });
    }
    get child_models() {
        return [];
    }
    _update_layout() {
        this.layout = new LayoutItem();
        this.layout.set_sizing(this.box_sizing());
    }
}
NGLView.__name__ = "NGLView";
export class ngl extends LayoutDOM {
    constructor(attrs) {
        super(attrs);
    }
    static init_ngl() {
        // This is usually boilerplate. In some cases there may not be a view.
        this.prototype.default_view = NGLView;
        this.define(({ String, Boolean, Any }) => ({
            spin: [Boolean, false],
            representation: [String],
            rcsb_id: [String],
            color_list: [Any],
            pdb_string: [String]
        }));
    }
}
ngl.__name__ = "ngl";
ngl.init_ngl();
//# sourceMappingURL=ngl_viewer2.js.map