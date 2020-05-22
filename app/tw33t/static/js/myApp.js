const HOST = 'http://localhost:8009';

window.onload = function () {
    var app = new Vue({
        el: '#myApp',
        data: {
            handleText: undefined,
            buttonDisabled: true,
            tweets: [],
            errors: []
        },
        watch: {
            handleText: function (val) {
                this.buttonDisabled = !(val && val.length > 0);
            }
        },
        methods: {
            btnClickHandler: function (event) {
                if (!this.buttonDisabled) {
                    $('.modal').modal('show');
                    fetch(`${HOST}/tweets?${$.param({handle: this.handleText})}`)
                    .then(function(res) {
                        return res.json();
                    })
                    .then(function(data) {
                        this.errors = [];
                        if (data.errors && data.errors.length > 0) {
                            throw data.errors.map(function(e ) {return e.message;})
                        }
                        this.tweets = data;
                        $('.modal').modal('hide');
                    }.bind(this))
                    .catch(function(errors) {
                        this.errors = errors;
                        $('.modal').modal('hide');
                    }.bind(this));

                }
                return false;
            },

        },
        delimiters: ['[[', ']]'] //Prevent messing with with Jinja's template interpolation.
    });
}