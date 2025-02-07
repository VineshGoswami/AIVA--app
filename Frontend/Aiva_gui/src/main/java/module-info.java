module com.vines.aiva.aiva_gui {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.web;


    opens com.vines.aiva.aiva_gui to javafx.fxml;
    exports com.vines.aiva.aiva_gui;
}