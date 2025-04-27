import { ref, onUnmounted } from "vue";
import { useAuth } from "@/stores/auth";
export function useNotifications(){
  const list = ref<any[]>([]);
  const { token } = useAuth();
  const es = new EventSource(`${import.meta.env.VITE_API_URL}/notifications/stream?token=${token}`);
  es.onmessage = e => list.value.unshift(JSON.parse(e.data));
  onUnmounted(()=>es.close());
  return { list };
}
