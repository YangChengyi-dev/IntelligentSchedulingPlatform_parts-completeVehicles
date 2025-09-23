export default {
  namespaced: true,
  state: {
    id: 0,
    user:{}
  },
  mutations: {
    updateId (state, id) {
      state.id = id
    },
    updateUser(state,user){
      state.user=user
    }
  }
}
