//
//  AppDelegate.m
//  FormulatePro
//
//  Created by Andrew de los Reyes on 7/5/06.
//  Copyright 2006 Andrew de los Reyes. All rights reserved.
//

#import "AppDelegate.h"

@implementation AppDelegate

- (BOOL)applicationShouldOpenUntitledFile:(NSApplication *)application
{
    return NO;
}

- (IBAction)showLicense:(id)sender
{
    NSString *path = [[NSBundle mainBundle] pathForResource:@"LICENSE" ofType:@"txt"];
    NSError *error = nil;
    NSString *license = [NSString stringWithContentsOfFile:path encoding:NSUTF8StringEncoding error:&error];
    if (!license) return;

    NSWindow *window = [[NSWindow alloc] initWithContentRect:NSMakeRect(0, 0, 500, 400)
                                                   styleMask:(NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable)
                                                     backing:NSBackingStoreBuffered
                                                       defer:NO];
    [window setTitle:@"License"];
    [window center];

    NSScrollView *scrollView = [[NSScrollView alloc] initWithFrame:[[window contentView] bounds]];
    [scrollView setAutoresizingMask:(NSViewWidthSizable | NSViewHeightSizable)];
    [scrollView setHasVerticalScroller:YES];

    NSTextView *textView = [[NSTextView alloc] initWithFrame:[[scrollView contentView] bounds]];
    [textView setEditable:NO];
    [textView setFont:[NSFont userFixedPitchFontOfSize:11]];
    [textView setBackgroundColor:[NSColor whiteColor]];
    [textView setTextColor:[NSColor blackColor]];
    [textView setAutoresizingMask:(NSViewWidthSizable | NSViewHeightSizable)];
    [[textView textStorage] beginEditing];
    [[textView textStorage] setAttributedString:[[NSAttributedString alloc] initWithString:license]];
    [[textView textStorage] endEditing];

    [scrollView setDocumentView:textView];
    [window setContentView:scrollView];
    [window setReleasedWhenClosed:NO];
    [window makeKeyAndOrderFront:nil];
}


- (void)removeUnwantedMenuItems
{
    NSMenu *mainMenu = [NSApp mainMenu];
    NSMenu *appMenu = [[mainMenu itemAtIndex:0] submenu];

    // Collect items to remove from the app menu
    NSMutableArray *itemsToRemove = [NSMutableArray array];
    for (NSMenuItem *item in [appMenu itemArray]) {
        NSString *title = [item title];
        if ([title containsString:@"Check for Update"] ||
            [title containsString:@"Bug"] ||
            [title containsString:@"bug"] ||
            [title containsString:@"Feedback"] ||
            [title containsString:@"feedback"]) {
            [itemsToRemove addObject:item];
        }
    }

    // Remove items and their preceding separators
    for (NSMenuItem *item in itemsToRemove) {
        NSInteger idx = [appMenu indexOfItem:item];
        [appMenu removeItem:item];
        if (idx > 0 && idx <= [appMenu numberOfItems] &&
            [[appMenu itemAtIndex:idx - 1] isSeparatorItem]) {
            [appMenu removeItemAtIndex:idx - 1];
        }
    }

    // Clean up any double separators left behind
    for (NSInteger i = [appMenu numberOfItems] - 1; i > 0; i--) {
        if ([[appMenu itemAtIndex:i] isSeparatorItem] &&
            [[appMenu itemAtIndex:i - 1] isSeparatorItem]) {
            [appMenu removeItemAtIndex:i];
        }
    }
}

- (void)removeCheckForUpdatesFromPreferences
{
    // Find and hide the "Check for new versions at startup" checkbox
    // in the Preferences window by walking all windows
    for (NSWindow *window in [NSApp windows]) {
        if ([[window title] containsString:@"Preferences"] ||
            [[window title] containsString:@"Settings"]) {
            [self removeUpdateCheckboxFromView:[window contentView]];
        }
    }
}

- (void)removeUpdateCheckboxFromView:(NSView *)view
{
    for (NSView *subview in [view subviews]) {
        if ([subview isKindOfClass:[NSButton class]]) {
            NSButton *button = (NSButton *)subview;
            NSString *title = [button title];
            if ([title containsString:@"Check for new versions"] ||
                [title containsString:@"Check for update"] ||
                [title containsString:@"SUCheckAtStartup"]) {
                [button setHidden:YES];
            }
        }
        [self removeUpdateCheckboxFromView:subview];
    }
}

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    [self removeUnwantedMenuItems];
    // Delay slightly to ensure Preferences window nib is loaded
    [self performSelector:@selector(removeCheckForUpdatesFromPreferences) withObject:nil afterDelay:0.5];
}

@end
