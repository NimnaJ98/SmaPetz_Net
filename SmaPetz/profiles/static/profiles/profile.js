console.log('hello world')

const followSuggestionBody = document.getElementById('follow-suggestions-body')
const spinnerBox = document.getElementById('spinner-box')

console.log('followSuggestionBody')
console.log('spinnerBox')

$.ajax({
    type: 'GET',
    url: '/profiles/user-json/',
    success: function(response){
        console.log(response)
    },
    error: function(error){
        console.log(error)
    }
})