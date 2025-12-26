<template>
  <el-dialog
    v-model="visible"
    title="设置"
    width="500px"
    :close-on-click-modal="false"
  >
    <el-form :model="form" label-width="100px">
      <el-form-item label="API Key">
        <el-input
          v-model="form.api_key"
          type="password"
          placeholder="请输入千问API Key"
          show-password
        />
      </el-form-item>
      
      <el-form-item label="地域选择">
        <el-radio-group v-model="form.region">
          <el-radio label="beijing">北京地域</el-radio>
          <el-radio label="singapore">新加坡地域</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-alert
        title="提示"
        type="info"
        :closable="false"
        style="margin-bottom: 20px"
      >
        <template #default>
          <p>获取API Key: https://help.aliyun.com/zh/model-studio/get-api-key</p>
          <p>新加坡和北京地域的API Key不同</p>
        </template>
      </el-alert>
    </el-form>
    
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="saveSettings" :loading="loading">
        保存
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useVoiceStore } from '@/stores/voice'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const voiceStore = useVoiceStore()
const { settings, saveSettings: saveSettingsApi, loadSettings } = voiceStore

const visible = ref(props.modelValue)
const loading = ref(false)
const form = ref({
  api_key: '',
  region: 'beijing'
})

watch(() => props.modelValue, (newVal) => {
  visible.value = newVal
  if (newVal) {
    loadSettingsData()
  }
})

watch(visible, (newVal) => {
  emit('update:modelValue', newVal)
})

const loadSettingsData = async () => {
  await loadSettings()
  form.value.api_key = settings.value.api_key || ''
  form.value.region = settings.value.region || 'beijing'
}

const saveSettings = async () => {
  if (!form.value.api_key) {
    ElMessage.warning('请输入API Key')
    return
  }
  
  loading.value = true
  try {
    await saveSettingsApi(form.value.api_key, form.value.region)
    ElMessage.success('设置保存成功')
    visible.value = false
  } catch (error) {
    ElMessage.error('设置保存失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadSettingsData()
})
</script>
