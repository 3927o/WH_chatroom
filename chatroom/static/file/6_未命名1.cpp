#include <iostream>
using namespace std;

int main(){
    int n,i,ans=1;
    cin>>n;
    for(i=2;i<n;i++){
        if(n%i==0) ans*=i;
    }
    cout<<ans<<endl;
    return 0;
}
