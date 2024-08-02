import { FlatList, SafeAreaView, StyleSheet, Text, TouchableOpacity, View, Platform } from "react-native";
import { useEffect, useRef, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { apiURL } from "../../App";
import { useNavigation } from "@react-navigation/native";
import Constants from "expo-constants";
import DateTimePickerModal from 'react-native-modal-datetime-picker';
import * as Device from 'expo-device';
import * as Notifications from 'expo-notifications';
import Icon from "react-native-ionicons";
import { Ionicons } from '@expo/vector-icons'; // Import Ionicons from Expo


Notifications.setNotificationHandler({
    handleNotification: async () => ({
      shouldShowAlert: true,
      shouldPlaySound: true,
      shouldSetBadge: false,
    }),
  });

export default function Home() {
    const times = {1:"8 am", 2: "9 am", 3: "10 : 30 am", 4: "11 : 30 am", 5: "1 pm", 6: "2 pm", 7:"3 pm", 8:"4 pm", 9:"5 pm", 10:"6 pm", 11:"7 pm", 12:"8 pm", 13:"9 pm", 14:"10 pm"}
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    const navigation = useNavigation();

    const date = new Date();
    const currentTime = date.getHours();
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    const today = date.getDay();
    console.log("td",today)
    const [ todaySchedule, setTodaySchedule ] = useState([]);
    const [ currentItem, setCurrentItem ] = useState([]);
    const [ firstElement, setFirstElement ] = useState([]);
    const [ isRefreshing, setIsrefreshing ] = useState(false);
    var data = []
    const [isDatePickerVisible, setDatePickerVisibility] = useState(false);
    const [selectedDate, setSelectedDate] = useState(null);

    const [expoPushToken, setExpoPushToken] = useState('');
    const [channels, setChannels] = useState<Notifications.NotificationChannel[]>([]);
    const [notification, setNotification] = useState<Notifications.Notification | undefined>(
      undefined
    );
    const notificationListener = useRef<Notifications.Subscription>();
    const responseListener = useRef<Notifications.Subscription>();

    const showDatePicker = () => {
        setDatePickerVisibility(true);
    };

    const hideDatePicker = () => {
        setDatePickerVisibility(false);
    };

    const handleConfirm = (new_date, dd) => {
      let ss
      let new_time = parseInt((new_date.getHours() * 60 * 60)) + parseInt((new_date.getMinutes() * 60));
      let c_time = parseInt(date.getHours() * 60 * 60) + parseInt(date.getMinutes()* 60);
      if(new_time > c_time) {
        ss = new_time - c_time;
      } else {
        ss = new_time + c_time;
      }
      // ss = parseInt(new_date.Time()/1000) - parseInt(date.Time()/1000);
      setSelectedDate(new_date);
      console.log("skn",new_date.getTime()/1000)
      schedulePushNotification(mm=dd, tt=ss)
      console.log("ss", new_time);
      hideDatePicker();
    };

    useEffect(() => {
        getStoredData();

        registerForPushNotificationsAsync().then(token => token && setExpoPushToken(token));

    if (Platform.OS === 'android') {
      Notifications.getNotificationChannelsAsync().then(value => setChannels(value ?? []));
    }
    notificationListener.current = Notifications.addNotificationReceivedListener(notification => {
      setNotification(notification);
    });

    responseListener.current = Notifications.addNotificationResponseReceivedListener(response => {
      console.log(response);
    });

    return () => {
      notificationListener.current &&
        Notifications.removeNotificationSubscription(notificationListener.current);
      responseListener.current &&
        Notifications.removeNotificationSubscription(responseListener.current);
    };
    },[])
    async function fetchData(departmentId, yearGroup, tableId) {
        try{
            setIsrefreshing(true);
            const response = await fetch(apiURL + '/schedules/?department_id=' + departmentId + '&format=json&timetable_id=' + tableId + '&year_group=' + yearGroup)
            if(!response) {
                console.log("Bad network");
            } else {
                const result = await response.json();
                data = await result;
                data = await data.filter((dt)=> dt.day == today);
                data = await data.sort((a,b) => a.time > b.time ? 1: -1);
                data = await data.filter((sd) => sd.time + 7 > currentTime);
                setFirstElement(await data.splice(0,1));
                setTodaySchedule(await data);
                setIsrefreshing(false);
            }
        } catch(error) {
            console.log("Error fetching data for home : ", error);
        }finally{
            
        }
    }
    async function getStoredData() {
        const storedDepartmentId = await AsyncStorage.getItem("departmentId")
        const storedYearGroup = await AsyncStorage.getItem("yearGroup");
        const storedTableId = await AsyncStorage.getItem("tableId");
        await fetchData(departmentId=storedDepartmentId, yearGroup=storedYearGroup, tableId=storedTableId);
    }
    console.log("f",todaySchedule)
    return(
        <SafeAreaView style={styles.container}>
            <View>
                <Text style={styles.dayText}>{days[today]}</Text>
                <Text style={styles.dateText}>{day} - {month} - {year}</Text>
                <Text style={styles.upcomingClassText}>Upcoming Class</Text>
                   
                    {firstElement.length > 0 && (
                    <View style={styles.firstElem}>    
                        <TouchableOpacity onPress={() => navigation.navigate('Details', { item: firstElement[0], times })}>
                            <Text style={styles.upcomingClassInfo}>{times[firstElement[0].time]}</Text>
                            <Text style={styles.classDetails}>{firstElement[0].course_code}</Text>
                            <Text style={styles.classDetails}>{firstElement[0].location_name}</Text>
                            <Text style={styles.classDetails}>{firstElement[0].lecturer_name}</Text>
                        </TouchableOpacity>
                        <TouchableOpacity onPress={showDatePicker} style={styles.notificationButton}>
                          <Ionicons name="notifications-circle-outline" color="blue" size={40} />
                        </TouchableOpacity>
                        <DateTimePickerModal
                            isVisible={isDatePickerVisible}
                            mode="time"
                            onConfirm={(some_date)=> handleConfirm(new_date=some_date,dd=firstElement)}
                            onCancel={hideDatePicker}
                        />
                    </View>    
                    )}
                     
                   
             </View>
            {todaySchedule.length > 0 && (
                <FlatList
                 data={todaySchedule}
                 keyExtractor={(item) => item.id}
                 onRefresh={() => getStoredData()} // Implement your refresh logic
                 refreshing={isRefreshing}
                 renderItem={({item}) => (
                     <View style={styles.scheduleItem}>
                         <TouchableOpacity onPress={() => navigation.navigate('Details', { item:item, times })}>
                             <Text style={styles.upcomingClassInfo}>{times[item.time]}</Text>
                             <Text style={styles.classDetails}>{item.location_name}</Text>
                             <Text style={styles.lecturerText}>{item.lecturer_name}</Text>
                         </TouchableOpacity>
                         <TouchableOpacity onPress={() => showDatePicker()}
                          style={{padding: 10}}
                          >
                         <Ionicons name="notifications-circle-outline" color="blue" size={40} />
                         </TouchableOpacity>
                     </View>
                 )}
                />
            )}
               
        </SafeAreaView>
        

    )
}

async function schedulePushNotification(mm, tt) {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: `You have ${mm[0].course_code} 📬`,
        body: `At ${mm[0].location_name}`,
        data: { data: 'goes here', test: { test1: 'more data' } },
      },
      
      trigger: { seconds: parseInt(tt) },
    });
    console.log(tt)
  }

async function registerForPushNotificationsAsync() {
    let token;
  
    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'Timely',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#FF231F7C',
      });
    }
  
    if (Device.isDevice) {
      const { status: existingStatus } = await Notifications.getPermissionsAsync();
      let finalStatus = existingStatus;
      if (existingStatus !== 'granted') {
        const { status } = await Notifications.requestPermissionsAsync();
        finalStatus = status;
      }
      if (finalStatus !== 'granted') {
        alert('Failed to get push token for push notification!');
        return;
      }
      // Learn more about projectId:
      // https://docs.expo.dev/push-notifications/push-notifications-setup/#configure-projectid
      // EAS projectId is used here.
      try {
        const projectId = '042d8b0b-d2bb-42ae-b814-13b19c792dec';
          Constants?.expoConfig?.extra?.eas?.projectId ?? Constants?.easConfig?.projectId;
        if (!projectId) {
          throw new Error('Project ID not found');
        }
        token = (
          await Notifications.getExpoPushTokenAsync({
            projectId,
          })
        ).data;
        console.log(token);
      } catch (e) {
        token = `${e}`;
      }
    } else {
      alert('Must use physical device for Push Notifications');
    }
  
    return token;
  }
  


const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        padding: 16,
    },
    dayText: {
        color: '#333',
        fontSize: 18,
        marginBottom: 8,
    },
    dateText: {
        color: '#666',
        fontSize: 14,
        marginBottom: 16,
    },
    upcomingClassText: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 16,
    },
    upcomingClassInfo: {
        fontSize: 16,
        color: '#007AFF',
        marginBottom: 8,
    },
    classDetails: {
        fontSize: 14,
        color: '#444',
        marginBottom: 4,
    },
    noClassesText: {
        fontWeight: 'bold',
        color: '#888',
    },
    scheduleItem: {
      flexDirection: 'row',
      justifyContent: 'space-between',
        marginVertical: 10,
        padding: 16,
        borderBottomWidth: 1,
        borderColor: '#ddd',
    },
    lecturerText: {
        fontSize: 12,
        color: '#888',
    },
    buttonText: {
      color: '#fff',
    },
    notificationButton: {
      // backgroundColor: '#1976d2',
      width: 100,
    },
    firstElem: {
      flexDirection: 'row',
      justifyContent: 'space-between',
    }
});
