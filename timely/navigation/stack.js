import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Home from "../screens/home/Home";
import Days from "../screens/schedule/Days";
import Daily from "../screens/schedule/Daily";
import Details from "../screens/schedule/Details";
import EditProfile from "../screens/profile/EditProfile";
import Profile from "../screens/profile/Profile";
import Notifications from "../screens/notification/Notifications";
import SignIn from "../screens/sign-in/SignIn";
import SignIn2 from "../screens/sign-in/SignIn2";


const Stack = createNativeStackNavigator();

// export const AllStack = ({navigation}) => {
//     <Stack.Navigator>
//         <Stack.Screen name="s1" component={}
//     </Stack.Navigator>
// }

export const HomeStack = ({navigation}) => {

    return(
        <Stack.Navigator>
            <Stack.Screen name="Home" component={Home}/>
        </Stack.Navigator>
    )
}

export const ScheduleStack = ({navigation}) => {

    return(
        <Stack.Navigator>
            <Stack.Screen name="Days" component={Days} />
            <Stack.Screen name="Daily" component={Daily} />
            <Stack.Screen name="Details" component={Details} />
        </Stack.Navigator>
    )
}

export const ProfileStack = ({navigation}) => {

    return(
        <Stack.Navigator>
            <Stack.Screen name="Profile" component={Profile} />
            <Stack.Screen name="EditProfile" component={EditProfile} />
        </Stack.Navigator>
    )
}

export const NotificationStack = ({navigation}) => {

    return(
        <Stack.Navigator>
            <Stack.Screen name="Notification" component={Notifications} />
        </Stack.Navigator>
    )
}

export const SignInStack = ({navigation}) => {

    return(
        <Stack.Navigator screenOptions={{
            headerShown: false,
        }}>
            <Stack.Screen name="SignInFirst" options={{
                title: "Sign In"
            }} component={SignIn} />
            <Stack.Screen name="SignInSec" options={{
                title: "Sign In"
            }} component={SignIn2} />
        </Stack.Navigator>
    )
}