var vm = new Vue({
	el: '#app',
	data(){
		return {
			data: [],
			backends: [
				{nombre: 'Seleccione Conexion', url:''},
				{nombre: 'Python', url: 'http://127.0.0.1:5000/Produccion/Sales/Money'},
				{nombre: 'C Sharp', url: ''},
				{nombre: 'Java', url:''},
				{nombre: 'Go', url:''},
				{nombre: 'Php', url:''}
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