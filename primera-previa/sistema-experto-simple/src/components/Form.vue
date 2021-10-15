<template>
  <form class="form" v-on:submit.prevent>
    <h4 class="text-start">Seleccione sus sintomas</h4>
    <div
      v-for="sintoma in sintomas"
      :key="sintoma.sintomas"
      class="form-check d-flex"
    >
      <input
        class="form-check-input"
        type="checkbox"
        :value="sintoma.sintomas"
        :id="sintoma.id"
        v-model="sintomasChequeados"
      />
      <label class="form-check-label mx-2" :for="sintoma.id">{{
        capitalize(sintoma.sintomas)
      }}</label>
    </div>
    <div class="d-flex mt-3">
      <button
        @click="$emit('on:click', sintomasChequeados)"
        class="btn btn-primary"
        value="Enviar"
      >
        Consultar
      </button>
    </div>
  </form>
</template>

<script>
export default {
  props: {
    hechos: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      sintomas: this.hechos.filter((hecho) => hecho.sintomas),
      sintomasChequeados: [],
    };
  },

  methods: {
    capitalize(word) {
      const lower = word.toLowerCase();
      return lower.charAt(0).toUpperCase() + lower.slice(1);
    },
  },
};
</script>

<style>
</style>