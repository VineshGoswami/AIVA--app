module com.vines.aiva.aiva {
    requires javafx.controls;
    requires javafx.fxml;

    opens com.vines.aiva.aiva to javafx.fxml;
    exports com.vines.aiva.aiva;
}
