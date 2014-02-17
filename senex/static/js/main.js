$(document).ready(function() {
    CustomForm.init();
    NotificationActions.init();
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
            e.preventDefault();
            self.customForm.submit();
        });
    }

};

var NotificationActions = {
    init: function() {
        this.bind();
    },

    bind: function() {
        var self = this;

        $('.close').click(function(e) {
            e.preventDefault();
            var closeDiv = $(e.target).closest('div');
            closeDiv.hide()
        });
    }
}