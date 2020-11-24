
var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        clientId: '',
        clientContact: '',
        clientAddress: '',
        clients: clients,
        quoteAgreeId: '',
        agreementDescrip: '',
        paymentConditionId: '',
        shippingTermId: '',
        currencyId: '',
        currencyCode: 'USD',
        currencySymbol: '$',
        currency: [],
        quotesAgreements: quotesAgreements,
        paymentConditions: paymentConditions,
        shippingTerms: shippingTerms,
        currencies: currencies,
        lastQuoteNumber: lastQuoteNumber,
        configData: configData,
        prodId: '',
        prodDetail: '',
        prodRefPrice: '',
        prodPrice: '',
        prodQuantity: '',
        prodGroup: '',
        products: products,
        inputGroupName: '',
        inputGroupTax: 0,
        groups: [],
        subtotal: 0,
        totalWeight: 0,
        total: 0,
        taxes: '',
    },
    methods: {

        updateClient() {

            client = this.getClientInfo(this.clientId);

            this.clientContact = client.fields.cfname + " " + client.fields.clname
            this.clientAddress = client.fields.address;

        },
        createNewGroup() {

            if (!this.inputGroupName) {
                alert('Group Name is required')
                return;
            }
            var id = this.groups.length + 1;
            var newGroup = {
                id: id,
                name: this.inputGroupName,
                taxPercentage: this.inputGroupTax,
                products: []
            };

            this.groups.push(newGroup);
            this.clearGroupInputs();

            return;
        },
        removeGroup(id) {

            position = this.getGroupPosition(id);

            this.groups.splice(position, 1);
            this.reOrderGroupPosition();
            this.updateTotals();
        },
        addProductToGroup(groupId) {

            this.prodGroup = groupId;

            if (!this.validateProductsInputs())
                return;

            var prodPositon = this.getProductPosition(this.prodId);
            var groupPositon = this.getGroupPosition(this.prodGroup);
            let product = Object.assign({},this.products[prodPositon]); // create a new object not reference

            if (!product) {
                alert('ERROR: Product not found');
                return;
            }

            product['id'] = this.groups[groupPositon].products.length + 1;
            product['detail'] = this.prodDetail;
            product['weight'] = this.prodQuantity * product.fields.weight;
            product['quantity'] = this.prodQuantity;
            product['price'] = this.prodPrice;
            product['total'] = this.prodQuantity * this.prodPrice;
            product['tax'] = this.calculatePercent(this.groups[groupPositon].taxPercentage, product['total']);

            this.groups[groupPositon].products.push(product);
            this.updateTotals();
            this.clearProdFields();
        },
        removeProductFromGroup(groupId, prodId) {

            groupPosition = this.getGroupPosition(groupId);

            for (var i = 0; i < this.groups[groupPosition].products.length; i++) {

                if (this.groups[groupPosition].products[i].id == prodId) {

                    this.groups[groupPosition].products.splice(i, 1);
                }
            }

            this.reOrderProductFromGroupPosition(groupPosition);
        },
        reOrderProductFromGroupPosition(groupPosition) {


            for (var i = 0; i < this.groups[groupPosition].products.length; i++) {

                this.groups[groupPosition].products[i].id = i + 1;
            }
        },
        reOrderGroupPosition() {

            for (var i = 0; i < this.groups.length; i++) {

                this.groups[i].id = i + 1;
            }
        },
        updateQuotesAgreement() {
            var quoteAgreement = this.quotesAgreements[this.getQuoteAgreementPosition(this.quoteAgreeId)]

            this.agreementDescrip = quoteAgreement.fields.description;
            this.paymentConditionId = quoteAgreement.fields.payment_condition;
            this.shippingTermId = quoteAgreement.fields.shipping_terms;
        },
        updateCurrency() {

            for (var i=0; i<this.currencies.length; i++) {

                if (this.currencies[i].pk == this.currencyId) {

                    this.currencyCode = this.currencies[i].fields.code;
                    this.currencySymbol = this.currencies[i].fields.symbol;
                }
            }
        },
        updateTotals() {

            var subtotal = 0;
            var taxes = 0;
            var total = 0;
            var totalWeight = 0;
            var products = [];
            for (var i = 0; i < this.groups.length; i++) {

                products = this.groups[i].products;

                for (var j = 0; j < products.length; j++) {

                    totalWeight += products[j].weight;
                    subtotal += products[j].total;
                    taxes += products[j].tax;
                }

                products = [];
            }

            total = subtotal + this.taxes;

            this.subtotal = subtotal;
            this.totalWeight = totalWeight;
            this.taxes = taxes;
            this.total = total;
        },
        /* 
        |   usefull methods
        */

        // Get Client Info
        getClientInfo(id) {

            for (var i = 0; i < this.clients.length; i++) {

                if (this.clients[i].pk == id) return this.clients[i];
            }

        },

        // Get product position in this.products
        getProductPosition(id) {

            for (var i = 0; i < this.products.length; i++) {

                if (this.products[i].pk == id) {

                    return i;
                }
            }
            alert('ERROR: Product position not found');
            return;
        },
        // Get Group position in this.groups
        getGroupPosition(id) {

            for (var i = 0; i < this.groups.length; i++) {

                if (this.groups[i].id == id) {

                    return i;
                }
            }
            alert('ERROR: Group position not found');
            return;
        },
        // Get Group position in this.groups
        getQuoteAgreementPosition(id) {

            for (var i = 0; this.quotesAgreements.length; i++) {

                if (this.quotesAgreements[i].pk == id) return i
            }

            alert('Quote Agreement position not found');
            return -1;
        },
        // Load product details to input
        loadProductDetail(prodId) {

            var prodPositon = this.getProductPosition(prodId);
            this.prodDetail = this.products[prodPositon].fields.detail;
            this.prodRefPrice = this.products[prodPositon].fields.price;
        },
        // Clear Group Input Fields
        clearGroupInputs() {

            this.inputGroupName = '';
            this.inputGroupTax = 0;
        },
        // Clear products input fields
        clearProdFields() {

            this.prodId = '';
            this.prodDetail = '';
            this.prodQuantity = '';
            this.prodPrice = '';
            this.prodGroup = '';
        },
        // validate products inputs
        validateProductsInputs() {

            var valid = false;

            if (this.prodId === '') alert('The Product id Field is required');
            else if (this.prodQuantity === '') alert('The Product Quiantity Field is required');
            else if (this.prodPrice === '') alert('The Product Price Field is required');
            else if (this.prodGroup === '') alert('The Product Group Field is required');
            else valid = true;

            return valid;
        },
        // Format currency number
        formatCurrencyNumber(value) {
            
          
            const options = { style: 'currency', currency: this.currencyCode };
           
            const numberFormat = new Intl.NumberFormat('en-US', options);

            return numberFormat.format(value);
        },
        numberFormat: function (x) {

            return x.toLocaleString(undefined, { minimumFractionDigits: 2 })
        },

        // Calculate Percentage
        calculatePercent: function(percent, num){
            return(percent / 100) * num;
        }
    },

    updated() {
        $('.selectpicker').selectpicker('refresh');
        this.updateTotals();
    }
})