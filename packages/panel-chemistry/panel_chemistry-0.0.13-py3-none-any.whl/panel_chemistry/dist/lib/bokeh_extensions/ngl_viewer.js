import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
export class NGLViewerView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.object.change, this.updateStage);
        this.connect(this.model.properties.extension.change, this.updateStage);
        this.connect(this.model.properties.representation.change, this.updateStage);
        this.connect(this.model.properties.color_scheme.change, this.updateParameters);
        this.connect(this.model.properties.custom_color_scheme.change, this.updateParameters);
        this.connect(this.model.properties.effect.change, this.updateEffect);
        this.connect(this.model.properties.background.change, this.setBackgroundcolor);
    }
    render() {
        super.render();
        this.el.id = "viewport";
        const wn = window;
        const ngl = wn.NGL;
        this._stage = new ngl.Stage(this.el);
        this.setBackgroundcolor();
        const stage = this._stage;
        this.updateStage();
        window.addEventListener("resize", function () {
            stage.handleResize();
        }, false);
    }
    setBackgroundcolor() {
        console.log(this.model.background);
        this._stage.setParameters({ backgroundColor: this.model.background });
    }
    after_layout() {
        super.after_layout();
        this._stage.handleResize();
    }
    updateEffect() {
        if (this.model.effect === "spin") {
            this._stage.setSpin(true);
        }
        else if (this.model.effect === "rock") {
            this._stage.setRock(true);
        }
        else {
            this._stage.setSpin(false);
            this._stage.setRock(false);
        }
    }
    getParameters() {
        if (this.model.color_scheme === "custom") {
            var list = this.model.custom_color_scheme;
            var scheme = NGL.ColormakerRegistry.addSelectionScheme(list, "new scheme");
            return { color: scheme };
        }
        else {
            return { colorScheme: this.model.color_scheme };
        }
    }
    updateParameters() {
        const parameters = this.getParameters();
        try {
            this._stage.compList[0].reprList[0].setParameters(parameters);
        }
        catch (e) {
            console.log(e);
        }
    }
    updateStage() {
        const model = this.model;
        this._stage.removeAllComponents();
        if (model.object === "") {
            return;
        }
        const parameters = this.getParameters();
        function finish(o) {
            o.addRepresentation(model.representation, parameters);
            o.autoView();
        }
        if (model.extension !== "") {
            this._stage.loadFile(new Blob([model.object], { type: 'text/plain' }), { ext: model.extension }).then(finish);
        }
        else if (model.object.includes("://")) {
            this._stage.loadFile(model.object).then(finish);
        }
        else {
            this._stage.loadFile("rcsb://" + model.object).then(finish);
        }
        // this.updateColor()
        this.updateEffect();
    }
}
NGLViewerView.__name__ = "NGLViewerView";
export class NGLViewer extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_NGLViewer() {
        this.prototype.default_view = NGLViewerView;
        this.define(({ String, Any }) => ({
            object: [String, ""],
            extension: [String, ""],
            representation: [String, "ribbon"],
            color_scheme: [String, "chainid"],
            custom_color_scheme: [Any, "chainid"],
            effect: [String, ""],
        }));
        this.override({
            height: 400,
            width: 600
        });
    }
}
NGLViewer.__name__ = "NGLViewer";
NGLViewer.__module__ = "panel_chemistry.bokeh_extensions.ngl_viewer";
NGLViewer.init_NGLViewer();
//# sourceMappingURL=ngl_viewer.js.map