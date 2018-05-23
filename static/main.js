var vm = new Vue({
	el: '#app',
	data(){
		return {
			data: [],
			backends: [
				{nombre: 'Seleccione Conexion', url:''},
				{nombre: 'Python  ', url: 'http://192.168.1.114:5000/inventory/stock'},
				{nombre: 'C Sharp',  url: 'http://192.168.1.110:5000/inventory/stock'},
				{nombre: 'Java',     url: 'http://192.168.1.111:5000/inventory/stock'},
				{nombre: 'Go',       url: 'http://192.168.1.112:5000/inventory/stock'},
				{nombre: 'Php 1',    url: 'http://192.168.1.113:5000/inventory/stock'},
				{nombre: 'NodeJs',   url: 'http://192.168.1.115:5000/inventory/stock'}	
			],
			filter:'',
			selected_backend: {nombre: 'Seleccione Conexion', url:''}
		}
	},
	computed: {
		filtredData: function(){
			var result = this.data
			var concatenatedValue = ''
			var searchValue = this.filter
			if (searchValue !== ''){
				result = this.data.filter(function(row){
					concatenatedValue =''
					Object.keys(row).forEach(function(key){
						concatenatedValue += row[key].toLowerCase()
					})
					return concatenatedValue.indexOf(searchValue.toLowerCase()) > -1;
				})
			}
			return result
		}
	},
	methods: {
		leerAPI(){
			if (!this.selected_backend.nombre || !this.selected_backend.url){
				alert('El backend elegido no posee una url de consulta');
				return;
			}
			axios.get(this.selected_backend.url, {
				
			}).then(response => {
				this.data = response.data
			}).catch(e => {
				console.log(e)
			})
		}
	},
	created(){
		
	}
})