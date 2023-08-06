// See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import { div } from "@bokehjs/core/dom";
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
export class JSMEEditorView extends HTMLBoxView {
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
        const container = div({ class: "jsme-editor", id: id });
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
JSMEEditorView.__name__ = "JSMEEditorView";
// The Bokeh .ts model corresponding to the Bokeh .py model
export class JSMEEditor extends HTMLBox {
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
JSMEEditor.__name__ = "JSMEEditor";
JSMEEditor.__module__ = "panel_chemistry.bokeh_extensions.jsme_editor";
JSMEEditor.init_JSMEEditor();
//# sourceMappingURL=jsme_editor.js.map