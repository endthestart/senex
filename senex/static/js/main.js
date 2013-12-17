$(document).ready(function() {
    CustomForm.init();
});

var CustomForm = {
    init: function() {
        this.submitButton = $(".addcart");
        this.customForm = $("#product-options-form");

        this.bind();
    },

    bind: function() {
        var self = this;

        self.submitButton.click(function(e) {
            e.preventDefault()
            console.log("awesome");
            self.customForm.submit();
        });
    }

};