
var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'hello',
        clientId: '',
        clientContact: '',
        clientAddress: '',
        clients: clients,
        quoteAgreeId: '',
        quotesAgreements: quotesAgreements,
        prodId: '',
        prodPrice: '',
        prodQuantity: '',
        prodGroup: '',
        products: products,
        inputGroupName: '',
        groups: [], 
    },
    methods: {

        updateClient() {

            client = this.getClientInfo(this.clientId);

            this.clientContact = client.fields.cfname + " " + client.fields.clname
            this.clientAddress = client.fields.address;

        },

        createNewGroup() {

            if (!this.inputGroupName) {
                alert('Debe ingresar nombre del Grupo')
                return;
            } 
            var id = this.groups.length + 1;
            var newGroup = {
                id: id,
                name: this.inputGroupName,
                products: []
            };
            this.groups.push(newGroup);
            this.inputGroupName='';
            return;
        },

        removeGroup(id) {

            position = this.getGroupPosition(id);

            this.groups.splice(position, 1);
        },

        addProductToGroup(groupId) {

            this.prodGroup = groupId;

            if (!this.validateProductsInputs())
                return;

            var prodPositon = this.getProductPosition(this.prodId);
            var groupPositon = this.getGroupPosition(this.prodGroup);
            var product = this.products[prodPositon];

            if (!product) {
                alert('ERROR: Product not found');
                return;
            }

            product['id'] = this.groups[groupPositon].products.length + 1;
            product['weight'] = this.prodQuantity * product.fields.weight;
            product['quantity'] = this.prodQuantity;
            product['price'] = this.prodPrice;
            product['total'] = this.prodQuantity * this.prodPrice;

            this.groups[groupPositon].products.push(product);
            this.clearProdFields();
        },

        removeProductFromGroup(groupId, prodId) {
            
        
            groupPosition = this.getGroupPosition(groupId);

            for (var i = 0; i < this.groups[groupPosition].products.length; i++) {
                
                if (this.groups[groupPosition].products[i].id == prodId) {

                    this.groups[groupPosition].products.splice(i,1);
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


        getProductPosition(id) {

            for (var i = 0; i < this.products.length; i++) {

                if (this.products[i].pk == id) {

                    return i;
                }
            }
            alert('ERROR: Product position not found');
            return;
        },
        
        getGroupPosition(id) {

            for (var i = 0; i < this.groups.length; i++) {

                if (this.groups[i].id == id) {

                    return i;
                }
            }
            alert('ERROR: Group position not found');
            return;
        },

        // Clear products input fields
        clearProdFields() {

            this.prodId= '';
            this.prodQuantity= '';
            this.prodPrice= '';
            this.prodGroup= '';
        },

        // validate products inputs

        validateProductsInputs() {

            var valid = false;

            if (this.prodId === '') alert('The Product id Field is required');
            else if (this.prodQuantity === '') alert('The Product Quiantity Field is required');
            else if (this.prodPrice === '') alert('The Product Price Field is required');
            else if (this.prodGroup === '') alert('The Product Group Field is required');
            else valid=true;

            return valid;
        }
    },

    updated() {

        $('.selectpicker').selectpicker('refresh');
    }
})