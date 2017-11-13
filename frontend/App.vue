<template>
	<div>
			<Top></Top>
			<router-view></router-view>
	</div>
		
</template>

<script>
import Top from './base/Top.vue'


export default {
	components: {
		Top,
	}
}
</script>

<style>
.blue {
    color: #4a90e2;
}
</style>
