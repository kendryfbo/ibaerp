
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
        quote: quote[0],
        quoteDetails: quoteDetails,
        quoteGroups: quoteGroups,
        quotesAgreements: quotesAgreements,
        paymentConditions: paymentConditions,
        shippingTerms: shippingTerms,
        currencies: currencies,
        prodId: '',
        prodDetail: '',
        prodRemarks: '',
        prodRefPrice: '',
        prodPrice: '',
        prodQuantity: '',
        prodNewId: 0,
        prodGroup: '',
        products: products,
        inputGroupName: '',
        inputGroupTax: 0,
        inputEditGroupName: '',
        inputEditTaxPercent: 0,
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
        loadEditGroup(groupName, GroupTaxPercent) {

            this.inputEditGroupName = groupName;
            this.inputEditTaxPercent = GroupTaxPercent;
        },
        editGroup(id) {

            position = this.getGroupPosition(id);

            this.groups[position].name = this.inputEditGroupName;
            this.groups[position].taxPercentage = this.inputEditTaxPercent;
            this.clearEditGroupInput();
        },
        clearEditGroupInput() {

            this.inputEditGroupName = '';
            this.inputEditTaxPercent = 0;
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
            product['remarks'] = this.prodRemarks;
            product['weight'] = this.prodQuantity * product.fields.weight;
            product['quantity'] = this.prodQuantity;
            product['price'] = this.prodPrice;
            product['total'] = this.prodQuantity * this.prodPrice;
            product['tax'] = this.calculatePercent(this.groups[groupPositon].taxPercentage, product['total']);

            this.groups[groupPositon].products.push(product);
            this.updateTotals();
            this.clearProdFields();
            this.reOrderProductFromGroupPosition(groupPositon);
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

            this.groups[groupPosition].products.sort((a, b) => parseInt(a.id) - parseInt(b.id));
        },
        reOrderGroupPosition() {

            for (var i = 0; i < this.groups.length; i++) {

                this.groups[i].id = i + 1;
            }
        },
        updateProductId(event, groupId, prodId) {

            event.preventDefault();
            groupPos = this.getGroupPosition(groupId);
            productPos = this.getProductPosInGroupId(groupId, prodId);
            this.groups[groupPos].products[productPos].id = event.target.value;
            this.reOrderProductFromGroupPosition(groupPos);

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
        |   Edit loads
        */
        loadQuote() {

            this.loadClient();
            this.loadGroups();
            this.loadProducts();
            this.loadPaymentCondition();
            this.loadShippingTerms();
            this.loadCurrency();
            this.agreementDescrip = this.quote.fields.description;
        },
        loadGroups() {

            for (var i=0; this.quoteGroups.length > i; i++) {

                var newGroup = {
                    id: this.quoteGroups[i].fields.group_num,
                    name: this.quoteGroups[i].fields.group_name,
                    taxPercentage: this.quoteGroups[i].fields.group_tax,
                    products: []
                };

                this.groups.push(newGroup);
            }
        },
        
        loadProducts() {

            for (var i = 0; this.quoteDetails.length > i; i++) {

                for (var j = 0; this.groups.length > j; j++) {
                    
                    if (this.groups[j].id == this.quoteDetails[i].fields.group_num ) {
                        
                        let prodPositon = this.getProductPosition(this.quoteDetails[i].fields.product)
                        let product = Object.assign({}, this.products[prodPositon]);
                        product['id'] =  this.quoteDetails[i].fields.item_num,
                        product['detail'] = this.quoteDetails[i].fields.product_detail,
                        product['remarks'] = this.quoteDetails[i].fields.product_remarks,
                        product['weight'] = Number(this.quoteDetails[i].fields.quantity * product.fields.weight);
                        product['quantity'] =  Number(this.quoteDetails[i].fields.quantity),
                        product['price'] =  Number(this.quoteDetails[i].fields.price),
                        product['total'] =  Number(this.quoteDetails[i].fields.subtotal),
                        product['tax'] =  Number(this.quoteDetails[i].fields.tax),
                     
                        this.groups[j].products.push(product);
                    }
                }
            }
        },

        loadClient() {
            this.clientId = this.quote.fields.client;
            this.updateClient()

        },
        loadPaymentCondition(){

            for (var i = 0; this.paymentConditions.length > i; i++) {
                
                if (this.paymentConditions[i].pk == this.quote.fields.payment_condition) {

                    this.paymentConditionId = this.paymentConditions[i].pk;                
                    return;
                }
            }
        },
        loadShippingTerms() {
            
            for (var i = 0; this.shippingTerms.length > i; i++) {

                if (this.shippingTerms[i].pk == this.quote.fields.shipping_term) {

                    this.shippingTermId = this.paymentConditions[i].pk;
                    return;
                }
            }
        },
        loadCurrency() {
            
            for (var i = 0; this.currencies.length > i; i++) {

                if (this.currencies[i].pk == this.quote.fields.currency) {

                    this.currencyId = this.currencies[i].pk;
                    return;
                }
            }
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
        getProductPosInGroupId(groupId, id) {

            groupPos = this.getGroupPosition(groupId);
            var products = this.groups[groupPos].products;
            for (var i = 0; i < products.length; i++) {

                if (products[i].id == id) {

                    return i;
                }
            }
            alert('ERROR: Product position not found on Group');
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
            this.prodRemarks = this.products[prodPositon].fields.remarks;
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
    },
    mounted() {
        this.loadQuote()
    }
})