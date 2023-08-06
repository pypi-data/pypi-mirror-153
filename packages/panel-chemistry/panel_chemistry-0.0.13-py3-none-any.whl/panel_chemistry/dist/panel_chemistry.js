/*!
 * Copyright (c) 2012 - 2022, Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */
(function(root, factory) {
  factory(root["Bokeh"], undefined);
})(this, function(Bokeh, version) {
  let define;
  return (function(modules, entry, aliases, externals) {
    const bokeh = typeof Bokeh !== "undefined" && (version != null ? Bokeh[version] : Bokeh);
    if (bokeh != null) {
      return bokeh.register_plugin(modules, entry, aliases);
    } else {
      throw new Error("Cannot find Bokeh " + version + ". You have to load it prior to loading plugins.");
    }
  })
({
"7e6ecbb3c3": /* index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require("tslib");
    const PanelChemistryExtensions = (0, tslib_1.__importStar)(require("1d64c18294") /* ./bokeh_extensions/ */);
    exports.PanelChemistryExtensions = PanelChemistryExtensions;
    const base_1 = require("@bokehjs/base");
    (0, base_1.register_models)(PanelChemistryExtensions);
},
"1d64c18294": /* bokeh_extensions\index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    var jsme_editor_1 = require("7b93e4c7bc") /* ./jsme_editor */;
    __esExport("JSMEEditor", jsme_editor_1.JSMEEditor);
    var ngl_viewer_1 = require("dfab2fc5c6") /* ./ngl_viewer */;
    __esExport("NGLViewer", ngl_viewer_1.NGLViewer);
},
"7b93e4c7bc": /* bokeh_extensions\jsme_editor.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    // See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    const dom_1 = require("@bokehjs/core/dom");
    function uuidv4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    const notSubscribed = "Not Subscribed";
    function readSDFValue(jsmeElement) {
        var data = jsmeElement.getMultiSDFstack();
        var output = "No multirecords SDF was pasted into the editor ";
        if (data.length > 0) {
            output = data.join("$$$$\n") + "$$$$\n";
        }
        return output;
    }
    function setModelValue(model, jsmeElement) {
        console.log("setValue - start", model.value);
        var value = model.value;
        if (model.format === "smiles") {
            console.log("getting smiles");
            value = jsmeElement.smiles();
            console.log("got smiles");
        }
        else if (model.format === "mol") {
            value = jsmeElement.molFile(false);
        }
        else if (model.format === "mol3000") {
            value = jsmeElement.molFile(true);
        }
        else if (model.format === "sdf") {
            value = readSDFValue(jsmeElement);
        }
        else {
            value = jsmeElement.jmeFile();
        }
        if (model.value !== value && value !== null) {
            console.log("setting value", value);
            model.value = value;
        }
        console.log("setValue - end", model.value);
    }
    function setModelValues(model, jsmeElement) {
        console.log("setValues - start");
        setModelValue(model, jsmeElement);
        setOtherModelValues(model, jsmeElement);
        console.log("setValues - end");
    }
    function resetOtherModelValues(model, jsmeElement) {
        if (!model.subscriptions.includes("jme")) {
            model.jme = notSubscribed;
        }
        if (!model.subscriptions.includes("smiles")) {
            model.smiles = notSubscribed;
        }
        if (!model.subscriptions.includes("mol")) {
            model.mol = notSubscribed;
        }
        if (!model.subscriptions.includes("mol3000")) {
            model.mol3000 = notSubscribed;
        }
        if (!model.subscriptions.includes("sdf")) {
            model.sdf = notSubscribed;
        }
        setModelValues(model, jsmeElement);
    }
    function cleanValue(value) {
        if (value === null) {
            return "null";
        }
        else {
            return value;
        }
    }
    function setOtherModelValues(model, jsmeElement) {
        console.log("setOtherValues - start");
        if (model.subscriptions.includes("jme")) {
            model.jme = cleanValue(jsmeElement.jmeFile());
        }
        if (model.subscriptions.includes("smiles")) {
            model.smiles = cleanValue(jsmeElement.smiles());
        }
        if (model.subscriptions.includes("mol")) {
            model.mol = cleanValue(jsmeElement.molFile(false));
        }
        if (model.subscriptions.includes("mol3000")) {
            model.mol3000 = cleanValue(jsmeElement.molFile(true));
        }
        if (model.subscriptions.includes("sdf")) {
            model.sdf = cleanValue(readSDFValue(jsmeElement));
        }
        console.log("setOtherValues - end");
    }
    // The view of the Bokeh extension/ HTML element
    // Here you can define how to render the model as well as react to model changes or View events.
    class JSMEEditorView extends html_box_1.HTMLBoxView {
        constructor() {
            super(...arguments);
            this.JSME = window.JSApplet.JSME;
            this.valueChanging = true;
        }
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.properties.value.change, () => {
                console.log("value change", this.model.value);
                if (!this.valueChanging) {
                    if (this.model.value === "") {
                        this.jsmeElement.reset();
                    }
                    else {
                        this.jsmeElement.readGenericMolecularInput(this.model.value);
                    }
                }
            });
            this.connect(this.model.properties.format.change, () => {
                console.log("format change", this.model.format);
                setModelValue(this.model, this.jsmeElement);
            });
            this.connect(this.model.properties.subscriptions.change, () => {
                console.log("subscriptions change", this.model.subscriptions);
                resetOtherModelValues(this.model, this.jsmeElement);
            });
            this.connect(this.model.properties.options.change, () => {
                console.log("options change", this.model.options);
                this.setJSMEOptions();
            });
            this.connect(this.model.properties.guicolor.change, () => {
                console.log("options change", this.model.options);
                this.setGUIColor();
            });
        }
        render() {
            console.log("render - start");
            super.render();
            const id = "jsme-" + uuidv4();
            const container = (0, dom_1.div)({ class: "jsme-editor", id: id });
            this.el.appendChild(container);
            this.jsmeElement = new this.JSME(id, this.getHeight(), this.getWidth(), {
                "options": this.model.options.join(","),
                "guicolor": this.model.guicolor
            });
            this.jsmeElement.readGenericMolecularInput(this.model.value);
            resetOtherModelValues(this.model, this.jsmeElement);
            setModelValues(this.model, this.jsmeElement);
            const this_ = this;
            function showEvent(event) {
                console.log("event", event);
                this_.valueChanging = true;
                setModelValues(this_.model, this_.jsmeElement);
                this_.valueChanging = false;
            }
            this.jsmeElement.setAfterStructureModifiedCallback(showEvent);
            console.log("render - end");
        }
        setGUIColor() {
            console.log("setGUIColor", this.model.guicolor);
            this.jsmeElement.setUserInterfaceBackgroundColor(this.model.guicolor);
        }
        setJSMEOptions() {
            const options = this.model.options.join(",");
            console.log("setJSMEOptions", options);
            this.jsmeElement.options(options);
        }
        getHeight() {
            if ((this.model.sizing_mode === "stretch_height" || this.model.sizing_mode === "stretch_both") && this.el.style.height) {
                return this.el.style.height;
            }
            else if (this.model.height) {
                return this.model.height.toString() + "px";
            }
            else {
                return "100px";
            }
        }
        getWidth() {
            if ((this.model.sizing_mode === "stretch_width" || this.model.sizing_mode === "stretch_both") && this.el.style.width) {
                return this.el.style.width;
            }
            else if (this.model.width) {
                return this.model.width.toString() + "px";
            }
            else {
                return "100px";
            }
        }
        resizeJSMEElement() {
            this.jsmeElement.setSize(this.getWidth(), this.getHeight());
        }
        after_layout() {
            super.after_layout();
            this.resizeJSMEElement();
        }
    }
    exports.JSMEEditorView = JSMEEditorView;
    JSMEEditorView.__name__ = "JSMEEditorView";
    // The Bokeh .ts model corresponding to the Bokeh .py model
    class JSMEEditor extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_JSMEEditor() {
            this.prototype.default_view = JSMEEditorView;
            this.define(({ String, Array }) => ({
                value: [String, ""],
                format: [String, ""],
                options: [Array(String), []],
                jme: [String, ""],
                smiles: [String, ""],
                mol: [String, ""],
                mol3000: [String, ""],
                sdf: [String, ""],
                subscriptions: [Array(String), []],
                guicolor: [String, "#c0c0c0"],
            }));
        }
    }
    exports.JSMEEditor = JSMEEditor;
    JSMEEditor.__name__ = "JSMEEditor";
    JSMEEditor.__module__ = "panel_chemistry.bokeh_extensions.jsme_editor";
    JSMEEditor.init_JSMEEditor();
},
"dfab2fc5c6": /* bokeh_extensions\ngl_viewer.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    class NGLViewerView extends html_box_1.HTMLBoxView {
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
    exports.NGLViewerView = NGLViewerView;
    NGLViewerView.__name__ = "NGLViewerView";
    class NGLViewer extends html_box_1.HTMLBox {
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
    exports.NGLViewer = NGLViewer;
    NGLViewer.__name__ = "NGLViewer";
    NGLViewer.__module__ = "panel_chemistry.bokeh_extensions.ngl_viewer";
    NGLViewer.init_NGLViewer();
},
}, "7e6ecbb3c3", {"index":"7e6ecbb3c3","bokeh_extensions/index":"1d64c18294","bokeh_extensions/jsme_editor":"7b93e4c7bc","bokeh_extensions/ngl_viewer":"dfab2fc5c6"}, {});});
//# sourceMappingURL=panel_chemistry.js.map
