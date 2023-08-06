from typing import overload
import Internal.Runtime.InteropServices
import System


class ComponentActivator(System.Object):
    """This class has no documentation."""

    def ComponentEntryPoint(self, args: System.IntPtr, sizeBytes: int) -> int:
        ...

    @staticmethod
    def GetFunctionPointer(typeNameNative: System.IntPtr, methodNameNative: System.IntPtr, delegateTypeNative: System.IntPtr, loadContext: System.IntPtr, reserved: System.IntPtr, functionHandle: System.IntPtr) -> int:
        """
        Native hosting entry point for creating a native delegate
        
        :param typeNameNative: Assembly qualified type name
        :param methodNameNative: Public static method name compatible with delegateType
        :param delegateTypeNative: Assembly qualified delegate type name
        :param loadContext: Extensibility parameter (currently unused)
        :param reserved: Extensibility parameter (currently unused)
        :param functionHandle: Pointer where to store the function pointer result
        """
        ...

    @staticmethod
    def LoadAssemblyAndGetFunctionPointer(assemblyPathNative: System.IntPtr, typeNameNative: System.IntPtr, methodNameNative: System.IntPtr, delegateTypeNative: System.IntPtr, reserved: System.IntPtr, functionHandle: System.IntPtr) -> int:
        """
        Native hosting entry point for creating a native delegate
        
        :param assemblyPathNative: Fully qualified path to assembly
        :param typeNameNative: Assembly qualified type name
        :param methodNameNative: Public static method name compatible with delegateType
        :param delegateTypeNative: Assembly qualified delegate type name
        :param reserved: Extensibility parameter (currently unused)
        :param functionHandle: Pointer where to store the function pointer result
        """
        ...


