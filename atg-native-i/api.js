export async function fetchData() {
    try {
        const response = await fetch('http://192.168.1.193:8000/api/schedules/');
        if(!response.ok) {
            throw new Error('Network response was not ok');
        }
        const result  = await response.json();
        return result;
    }
    catch(error) {
        console.error('Error fetching data: ', error);
    }
}